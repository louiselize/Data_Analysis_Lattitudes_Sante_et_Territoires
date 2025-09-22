import re
import pandas as pd
from pathlib import Path


def find_header_row(xlsx_path: str, sheet_name: str, max_scan: int = 50) -> int:
    """Retourne l'indice de la ligne d'entête (celle qui contient 'Code commune INSEE')."""
    tmp = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, dtype=str)
    for i in range(min(max_scan, len(tmp))):
        row_vals = " ".join(str(v) for v in tmp.iloc[i].tolist())
        if "Code commune INSEE" in row_vals:
            return i
    raise RuntimeError(f"Ligne d'entête introuvable dans la feuille '{sheet_name}'.")


def load_apl_from_sheet(xlsx_path: str, sheet_name: str, year: int) -> pd.DataFrame:
    # Trouver dynamiquement la ligne d'entête
    header_row = find_header_row(xlsx_path, sheet_name)

    # Lire la feuille avec la bonne ligne d'entête
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=header_row, dtype=str)

    # Renommer proprement les 6 colonnes attendues (en se basant sur l'ordre du fichier DREES)
    # On garde explicitement les 6 premières colonnes non vides
    expected_cols = [
        "code_insee",
        "commune",
        "apl_generalistes",
        "apl_generalistes_moins65",
        "pop_standardisee",
        "pop_totale",
    ]
    # parfois il y a des colonnes vides à droite -> on filtre
    df = df.loc[:, df.columns[:6]].copy()
    df.columns = expected_cols

    # Drop des lignes vides (ex: en-têtes répétées, totaux éventuels)
    df = df[df["code_insee"].notna()].copy()

    # Nettoyage des numériques : espaces insécables, espaces milliers, virgules
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
            .str.replace(" ", "", regex=False)  # espace classique (séparateur milliers)
            .str.replace(",", ".", regex=False)  # virgule décimale -> point
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Code INSEE : garder comme chaîne (préserve les zéros initiaux)
    df["code_insee"] = df["code_insee"].astype(str).str.strip()

    # Ajouter l'année
    df["annee"] = int(year)

    # Enlever des lignes fantômes (code_insee = 'nan' par ex.)
    df = df[~df["code_insee"].str.lower().isin(["nan", ""])]

    return df


if __name__ == "__main__":
    xlsx_path = "data/raw/apl-thierache-centre/apl_generalistes.xlsx"
    out_dir = Path("data/preprocessed/apl-thierache-centre/")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Lis la feuille APL 2022
    df2022 = load_apl_from_sheet(xlsx_path, sheet_name="APL 2022", year=2022)
    df2022.to_csv(out_dir / "apl_generalistes_2022.csv", index=False)

    print(
        "✅ Export -> data/preprocessed/apl-thierache-centre/apl_generalistes_2022.csv"
    )
    print(df2022.head())

    df2023 = load_apl_from_sheet(xlsx_path, sheet_name="APL 2023", year=2023)
    df2023.to_csv(out_dir / "apl_generalistes_2023.csv", index=False)

    print(
        "✅ Export -> data/preprocessed/apl-thierache-centre/apl_generalistes_2023.csv"
    )
    print(df2023.head())
