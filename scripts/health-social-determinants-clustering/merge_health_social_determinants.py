import pandas as pd


def charger_les_donnees():
    print(
        pd.read_csv(
            "data/raw/health-social-determinants-clustering/social_determinants.csv",
            sep=";",
            header=2,
        ).columns
    )
    df_social = pd.read_csv(
        "data/raw/health-social-determinants-clustering/social_determinants.csv",
        sep=";",
        header=2,
    ).rename(
        columns={
            "Code": "code",
            "Libellé": "libelle",
            "Nombre de décès domiciliés 2024": "deces_domicilies_2024",
            "Part des pers. âgées de 75 ans ou + 2022": "part_75_ans_plus",
            "Taux de pauvreté 2021": "taux_pauvrete",
            "Médiane du niveau de vie 2021": "revenu_median",
            "Part des non ou peu diplômés dans la pop. non scolarisée de 15 ans ou + 2022": "part_sans_diplome",
            "Part des ouvriers dans le nb d’emplois au LT 2022": "part_ouvriers",
            "Part des familles monoparentales 2022": "part_familles_monoparentales",
            "Part des pers. âgées de - 15 ans 2022": "part_moins_15_ans",
            "Taille moyenne des ménages 2022": "taille_menage",
            "Part des locataires dans les rés. principales 2022": "part_locataires",
            "Part des locataires HLM dans les rés. principales 2022": "part_locataires_HLM",
            "Part des résidences principales en suroccupation accentuée 2022": "part_suroccupation",
            "Part des rés. principales dans le total des logements 2022": "part_residences_principales",
            "Part des appartements dans le total des logements 2022": "part_appartements",
            "Part des maisons dans le total des logements 2022": "part_maisons",
            "Densité de population (historique depuis 1876) 2022": "densite_population",
        }
    )
    print(df_social.columns)
    df_sante = pd.read_csv(
        "data/raw/health-social-determinants-clustering/health.csv",
        sep=";",
        header=2,
    ).rename(
        columns={
            "Code": "code",
            "Libellé": "libelle",
            "Part des bénéf. ophtalmo. dans pop. 2024": "part_benef_ophtalmo",
            "APL Médecins généralistes 2023": "apl_generaliste",
            "Densité d'orthophonistes lib. 2024": "densite_orthophonistes",
            "Densité de généralistes lib. 2024": "densite_generalistes",
            "Densité d'infirmiers lib. 2024": "densite_infirmiers",
            "Densité de sages-femmes lib. 2024": "densite_sages_femmes",
            "Part des bénéf. en ALD dans la pop 2024": "part_benef_ald",
            "Densité des pharmacies pour 10 000 hab. 2024": "densite_pharmacies",
        }
    )
    print(df_sante.columns)

    return df_social, df_sante


def fusionner_et_nettoyer(df_social, df_sante):
    df_merged = pd.merge(df_social, df_sante, on="code", how="inner")

    df_merged["libelle"] = df_merged["libelle_x"].combine_first(df_merged["libelle_y"])
    df_merged = df_merged.drop(columns=["libelle_x", "libelle_y"])

    colonnes_numeriques = [
        # Sociales
        "deces_domicilies_2024",
        "part_75_ans_plus",
        "taux_pauvrete",
        "revenu_median",
        "part_sans_diplome",
        "part_ouvriers",
        "part_familles_monoparentales",
        "part_moins_15_ans",
        "taille_menage",
        "part_locataires",
        "part_locataires_HLM",
        "part_suroccupation",
        "part_residences_principales",
        "part_appartements",
        "part_maisons",
        "densite_population",
        # Santé
        "apl_generaliste",
        "part_benef_ophtalmo",
        "densite_orthophonistes",
        "densite_generalistes",
        "densite_infirmiers",
        "densite_sages_femmes",
        "part_benef_ald",
        "densite_pharmacies",
    ]

    for col in colonnes_numeriques:
        df_merged[col] = pd.to_numeric(df_merged[col], errors="coerce")

    df_merged = df_merged.dropna(subset=["apl_generaliste"])

    return df_merged


def main():
    df_social, df_sante = charger_les_donnees()
    df_final = fusionner_et_nettoyer(df_social, df_sante)

    output_path = "data/preprocessed/health-social-determinants-clustering/health_social_determinants.csv"
    df_final.to_csv(output_path, index=False, sep=";")


if __name__ == "__main__":
    main()
