import pandas as pd
from pathlib import Path

# --- chemins ---
XLSX_PATH = (
    "data/raw/apl-thierache-centre/apl_generalistes.xlsx"  # classeur source DREES
)
THIERACHE_PATH = "data/raw/apl-thierache-centre/communes_thierache_centre.csv"  # Commune,Code_INSEE,Code_postal
OUT_PATH = (
    "data/preprocessed/apl-thierache-centre/apl_generalistes_2022_2023_Thierache.csv"
)

SHEETS = [("APL 2022", 2022), ("APL 2023", 2023)]  # noms exacts des feuilles et année


def find_header_row(xlsx_path: str, sheet_name: str, max_scan: int = 50) -> int:
    """Retourne l'index de la ligne d'entête (celle qui contient 'Code commune INSEE')."""
    tmp = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, dtype=str)
    for i in range(min(max_scan, len(tmp))):
        row_vals = " ".join(str(v) for v in tmp.iloc[i].tolist())
        if "Code commune INSEE" in row_vals:
            return i
    raise RuntimeError(f"Ligne d'entête introuvable dans la feuille '{sheet_name}'.")


def load_apl_from_sheet(xlsx_path: str, sheet_name: str, year: int) -> pd.DataFrame:
    header_row = find_header_row(xlsx_path, sheet_name)
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=header_row, dtype=str)

    # On garde explicitement les 6 premières colonnes du tableau
    df = df.loc[:, df.columns[:6]].copy()
    df.columns = [
        "code_insee",
        "commune",
        "apl_generalistes",
        "apl_generalistes_moins65",
        "pop_standardisee",
        "pop_totale",
    ]

    # Supprimer les lignes vides / entêtes répétées
    df = df[df["code_insee"].notna()].copy()
    df["code_insee"] = df["code_insee"].astype(str).str.strip().str.zfill(5)

    # Nettoyage nombres (espaces insécables, séparateur de milliers, virgule décimale)
    for col in [
        "apl_generalistes",
        "apl_generalistes_moins65",
        "pop_standardisee",
        "pop_totale",
    ]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("\u00a0", "", regex=True)  # espace insécable
            .str.replace(" ", "", regex=False)  # espaces classiques
            .str.replace(",", ".", regex=False)  # virgule -> point
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["annee"] = int(year)
    df = df[~df["code_insee"].str.lower().isin(["nan", ""])]
    return df


def load_thierache_list(path: str) -> pd.DataFrame:
    # Fichier au format: Commune,Code_INSEE,Code_postal
    th = pd.read_csv(path, dtype={"Code_INSEE": str})
    th["Code_INSEE"] = th["Code_INSEE"].str.strip().str.zfill(5)
    th = th.rename(columns={"Code_INSEE": "code_insee"})
    return th[["code_insee"]].drop_duplicates().assign(is_thierache_centre=True)


def main():
    Path("data/preprocessed").mkdir(parents=True, exist_ok=True)

    # 1) Lire et empiler 2022 + 2023
    frames = [load_apl_from_sheet(XLSX_PATH, sheet, year) for sheet, year in SHEETS]
    apl_panel = pd.concat(frames, ignore_index=True)

    # 2) Charger la liste Thiérache et faire le flag
    th_flag = load_thierache_list(THIERACHE_PATH)
    apl_panel = apl_panel.merge(th_flag, on="code_insee", how="left")
    apl_panel["is_thierache_centre"] = apl_panel["is_thierache_centre"].fillna(False)

    # 3) Ordonner les colonnes
    ordered = [
        "annee",
        "code_insee",
        "commune",
        "is_thierache_centre",
        "apl_generalistes",
        "apl_generalistes_moins65",
        "pop_standardisee",
        "pop_totale",
    ]
    apl_panel = apl_panel[ordered]

    # 4) Export
    apl_panel.to_csv(OUT_PATH, index=False)
    print(f"✅ Export -> {OUT_PATH}")
    print(apl_panel.head())


if __name__ == "__main__":
    main()
