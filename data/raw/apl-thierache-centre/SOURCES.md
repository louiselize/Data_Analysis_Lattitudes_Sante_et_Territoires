# communes_thierache_centre.csv — origine et sources

Fichier généré et fourni par ChatGPT.  
Contenu : nom de la commune, code INSEE, code postal.

Sources utilisées pour constituer la liste :

- INSEE — Intercommunalité « La Thiérache du Centre » (EPCI 240200444).  
  https://www.insee.fr/fr/metadonnees/geographie/intercommunalite/240200444-la-thierache-du-centre
- Comersis — Export des communes par intercommunalité.  
  https://www.comersis.com/geo/geo/export-epci.php?dpt=02&epci=240200444

Remarque : les codes postaux indiqués correspondent à la correspondance principale et peuvent recouvrir plusieurs communes ou secteurs postaux.

---

# apl_generalistes.xlsx — origine et sources

Fichier brut téléchargé depuis le site de la DREES.  
Contenu : indicateurs d’accessibilité potentielle localisée (APL) aux médecins généralistes, par commune, pour les millésimes 2022 et 2023.

Source officielle :

- Ministère des Solidarités et de la Santé (DREES)  
  https://data.drees.solidarites-sante.gouv.fr/explore/dataset/530_l-accessibilite-potentielle-localisee-apl/information/

Remarque : ce fichier contient plusieurs feuilles (par année), avec des lignes de métadonnées introductives.  
Un script de prétraitement (`scripts/preprocess_apl.py`) est utilisé pour nettoyer et transformer ces données en un format exploitable (CSV).
