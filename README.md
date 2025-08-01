# Chemical Structure Analyzer

A lightweight Python-based tool to **fetch chemical structure information** (SMILES) from public chemical databases like **PubChem**, **ChEMBL**, and **DrugBank**, and analyze **aromaticity** using **RDKit**.

This tool helps researchers, chemists, and students quickly retrieve molecular data and visualize structures — ideal for early-stage cheminformatics workflows.

---

##  Features

- 🔍 Fetch canonical SMILES strings from:
  - **PubChem**
  - **ChEMBL**
  - **DrugBank** (optional API key)
- 🔬 Analyze aromatic rings using RDKit
- 🖼️ Generate and save 2D structure diagrams (`structure.png`)
- 📦 Clean CLI interaction for ease of use

---

## Requirements

- Python 3.7+
- `requests`
- `rdkit`

Install them using:

```bash
pip install -r requirements.txt

Or manually:
pip install requests
conda install -c conda-forge rdkit

usage :
python3 chemical_structure_analyzer.py



Example Output

Fetching from PubChem...
Fetching from ChEMBL...

PubChem SMILES Result:
CC(=O)OC1=CC=CC=C1C(=O)O

ChEMBL SMILES Result:
CC(=O)OC1=CC=CC=C1C(=O)O

Analyzing aromaticity...
Aromatic rings: 1
2D structure saved as: structure.png


📧 Contact
Author: M. Sakib Abdullah
Email: mohdsakib219@gmail.com
Feel free to contribute or suggest improvements!


```bash
pip install -r requirements.txt
