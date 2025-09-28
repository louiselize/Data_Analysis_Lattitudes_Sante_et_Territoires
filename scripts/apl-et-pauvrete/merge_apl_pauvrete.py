import pandas as pd


def charger_les_donnees():
    df_pauvrete = pd.read_csv(
        "data/raw/apl-et-pauvrete/taux_pauvrete_2021.csv", sep=";", header=2
    ).rename(
        columns={
            "Code": "code",
            "Libellé": "libelle",
            "Taux de pauvreté 2021": "taux_pauvrete",
        }
    )

    df_apl = pd.read_csv(
        "data/raw/apl-et-pauvrete/apl_medecins_generalistes_2023.csv",
        sep=";",
        header=2,
    ).rename(
        columns={
            "Code": "code",
            "Libellé": "libelle",
            "APL Médecins généralistes 2023": "apl_generaliste",
        }
    )

    return df_apl, df_pauvrete


def fusionner_et_filtrer(df_apl, df_pauvrete):
    df_merged = pd.merge(df_apl, df_pauvrete, on="code", how="outer")

    df_merged["libelle"] = df_merged["libelle_x"].combine_first(df_merged["libelle_y"])
    df_merged = df_merged.drop(columns=["libelle_x", "libelle_y"])

    df_merged = df_merged[["code", "libelle", "apl_generaliste", "taux_pauvrete"]]

    df_merged["apl_generaliste"] = pd.to_numeric(
        df_merged["apl_generaliste"], errors="coerce"
    )
    df_merged["taux_pauvrete"] = pd.to_numeric(
        df_merged["taux_pauvrete"], errors="coerce"
    )

    df_merged = df_merged.dropna(subset=["apl_generaliste", "taux_pauvrete"], how="any")

    return df_merged


def main():
    df_apl, df_pauvrete = charger_les_donnees()
    df_final = fusionner_et_filtrer(df_apl, df_pauvrete)

    output_path = "data/preprocessed/apl-et-pauvrete/apl_et_pauvrete.csv"
    df_final.to_csv(output_path, index=False, sep=";")


if __name__ == "__main__":
    main()
