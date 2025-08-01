import requests
from rdkit import Chem
from rdkit.Chem import Draw
import json
import os

def get_smiles_from_pubchem(compound_name):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound_name}/property/CanonicalSMILES/JSON"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        smiles = data['PropertyTable']['Properties'][0]['CanonicalSMILES']
        return smiles
    except (KeyError, IndexError):
        return "Error: SMILES not found in PubChem response."
    except Exception as e:
        return f"Error from PubChem: {e}"

def get_smiles_from_chembl(compound_name):
    try:
        search_url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/search.json?q={compound_name}"
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        molecules = data.get('molecules', [])
        if not molecules:
            return f"No results for '{compound_name}' in ChEMBL."

        for mol in molecules:
            chembl_id = mol.get('molecule_chembl_id')
            if chembl_id:
                detail_url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
                detail_resp = requests.get(detail_url)
                detail_resp.raise_for_status()
                mol_data = detail_resp.json()
                return mol_data.get('molecule_structures', {}).get('canonical_smiles', "SMILES not available.")
        return "No valid SMILES found."
    except Exception as e:
        return f"Error from ChEMBL: {e}"

def get_smiles_from_drugbank(compound_name, api_key):
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        url = f"https://api.drugbank.com/v1/structures/search?query={compound_name}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['structures'][0]['smiles'] if data['structures'] else "No DrugBank SMILES found."
    except Exception as e:
        return f"Error from DrugBank: {e}"

def analyze_aromaticity(smiles, save_image=True, img_name="structure.png"):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return "Invalid SMILES for aromaticity analysis."

        aromatic_rings = sum(
            all(mol.GetAtomWithIdx(i).GetIsAromatic() for i in ring)
            for ring in mol.GetRingInfo().AtomRings()
        )

        if save_image:
            img = Draw.MolToImage(mol)
            img.save(img_name)

        return {
            "aromatic_rings": aromatic_rings,
            "structure_file": img_name if save_image else None
        }
    except Exception as e:
        return f"Error in aromaticity analysis: {e}"

def main():
    print("🔬 Welcome to the Enhanced Chemical Structure Analyzer 🔍")
    compound_name = input("Enter the IUPAC or common name of the compound: ").strip()
    drugbank_api_key = input("Enter your DrugBank API key (press Enter to skip DrugBank): ").strip()

    results = {}

    print("\nFetching from PubChem...")
    results['PubChem'] = get_smiles_from_pubchem(compound_name)

    print("Fetching from ChEMBL...")
    results['ChEMBL'] = get_smiles_from_chembl(compound_name)

    if drugbank_api_key:
        print("Fetching from DrugBank...")
        results['DrugBank'] = get_smiles_from_drugbank(compound_name, drugbank_api_key)

    for source, result in results.items():
        print(f"\n{source.upper()} SMILES Result:")
        print(result)

        if isinstance(result, str) and not result.startswith("Error") and "No" not in result:
            print(f"Analyzing aromaticity for {source} compound...")
            analysis = analyze_aromaticity(result)
            if isinstance(analysis, dict):
                print(f"Aromatic rings: {analysis['aromatic_rings']}")
                if analysis['structure_file']:
                    print(f"2D structure saved as: {analysis['structure_file']}")
            else:
                print(analysis)

if __name__ == "__main__":
    main()

