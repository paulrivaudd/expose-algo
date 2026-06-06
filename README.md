# Prototype de base de données — skip-list vs red-black tree

Projet d'algo, séance 5. Comparaison de deux structures de données ordonnées
sur le dataset adult_train.

## Lancer

```bash
python main.py adult_train.csv
```

Le CSV se télécharge ici :
https://github.com/selva86/datasets/blob/master/adult_train.csv

## Fichiers

- `data_loader.py` — lecture du CSV, modèle `Person`
- `skiplist.py` — la skip-list
- `rbtree.py` — l'arbre rouge-noir
- `database.py` — wrapper "base de données" qui utilise l'une ou l'autre
- `compare_perf.py` — mesures de performance
- `main.py` — point d'entrée
- `gen_test_csv.py` — génère un faux CSV si besoin de tester sans le vrai

## Requêtes testées

- `find_by_id(id)` — recherche exacte par identifiant
- `find_by_age(age)` — toutes les personnes d'un âge donné
- `find_by_age_range(a, b)` — range query
- `count_high_income_in_age_range` — range + filtre
