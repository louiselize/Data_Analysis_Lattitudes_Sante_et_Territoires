# Défi : Santé et Territoires 🏥

This repository is part of **Season 4 of the Open Data University (ODU)**, an initiative by [Latitudes](https://www.latitudes.cc/) to foster responsible and impactful uses of open data in higher education.

As a volunteer _référent défi_, my role is to explore datasets, create resources, and support students and teachers working on the **"Santé et Territoires" challenge**. The focus is on healthcare access, social determinants of health, and identifying territorial vulnerabilities in France.

👉 All project deliverables and documentation will be in **French**.

## 📂 Repository structure

The project is organized as follows:

```
Data_Analysis_Latitudes_Sante_et_Territoires/
│
├── data/
│   ├── raw/            # Raw datasets (directly downloaded, unmodified)
│   └── preprocessed/   # Cleaned or filtered datasets
│
├── notebooks/          # Jupyter notebooks for exploration and analysis
│
├── scripts/            # Python scripts for preprocessing and merging datasets
│
├── analysis/           # Results of analyses (figures, tables, reports)
│
└── README.md           # Project description
```

👉 This structure helps to:

- Keep raw data intact for reproducibility.
- Separate data processing (`scripts/`) from analysis (`notebooks/`).
- Store all deliverables and results in a clear location (`analysis/`).

### ⚙️ Installing Dependencies

To run this project locally, you need to install the required Python libraries.
They are listed in the [`requirements.txt`](./requirements.txt) file.

```bash
pip install -r requirements.txt
```

💡 **Tip**: It's best to install them inside a **virtual environment** to avoid version conflicts.

Example using `venv`:

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
