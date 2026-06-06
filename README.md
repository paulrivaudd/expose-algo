# Prototype de base de données — Skip-List vs Red-Black Tree

> Implémentation et comparaison de performances de deux structures de données ordonnées appliquées à un moteur de requêtes sur un dataset réel (UCI Adult Census, ~32 000 entrées).

---

## Contexte

Ce projet explore deux structures de données classiques en algorithmique pour implémenter un moteur de base de données minimaliste :

- **Skip-List** — structure probabiliste en liste chaînée multi-niveaux. Complexité moyenne O(log n) pour la recherche, l'insertion et la suppression.
- **Red-Black Tree** — arbre binaire de recherche auto-équilibré. Complexité garantie O(log n) dans le pire cas.

L'objectif est de comparer leurs performances sur des requêtes réelles : recherche exacte, requêtes par plage (range queries), et requêtes filtrées.

---

## Complexités comparées

| Opération         | Skip-List (moy.) | Skip-List (pire) | Red-Black Tree |
|-------------------|-----------------|-----------------|----------------|
| Recherche         | O(log n)        | O(n)            | O(log n)       |
| Insertion         | O(log n)        | O(n)            | O(log n)       |
| Suppression       | O(log n)        | O(n)            | O(log n)       |
| Range query       | O(log n + k)    | O(n)            | O(log n + k)   |
| Espace mémoire    | O(n log n)      | O(n log n)      | O(n)           |

*k = nombre d'éléments dans l'intervalle*

---

## Dataset

**UCI Adult Census Income** (`adult_train.csv`) — ~32 000 entrées représentant des individus avec attributs : âge, profession, niveau d'éducation, revenu (>50K / ≤50K).

```
age, workclass, fnlwgt, education, education-num, marital-status,
occupation, relationship, race, sex, capital-gain, capital-loss,
hours-per-week, native-country, class
```

---

## Requêtes implémentées

```python
db.find_by_id(id)                          # Recherche exacte par identifiant
db.find_by_age(age)                        # Toutes les personnes d'un âge donné
db.find_by_age_range(a, b)                 # Range query sur l'âge
db.count_high_income_in_age_range(a, b)    # Range query + filtre sur le revenu
```

---

## Structure du projet

```
expose-algo/
├── skiplist.py       # Implémentation complète de la skip-list
├── rbtree.py         # Implémentation de l'arbre rouge-noir
├── database.py       # Abstraction "base de données" (skip-list ou RBT)
├── data_loader.py    # Chargement du CSV, modèle Person
├── compare_perf.py   # Benchmarks et mesures de performance
├── main.py           # Point d'entrée — démo des requêtes
└── adult_train.csv   # Dataset UCI Adult Census
```

---

## Lancer le projet

```bash
# Cloner le repo
git clone https://github.com/paulrivaud/expose-algo.git
cd expose-algo

# Lancer la démo
python main.py adult_train.csv

# Lancer les benchmarks de performance
python compare_perf.py adult_train.csv
```

> Le dataset peut aussi être téléchargé ici : [UCI Adult Census](https://github.com/selva86/datasets/blob/master/adult_train.csv)

---

## Résultats

Les benchmarks (`compare_perf.py`) mesurent le temps d'exécution de chaque type de requête sur les deux structures après chargement complet du dataset (~32 000 entrées).

Points clés observés :
- Le **Red-Black Tree** est plus performant sur les **range queries** grâce à sa traversée in-order garantie en O(log n + k)
- La **Skip-List** offre une implémentation plus simple et des performances comparables en pratique sur les recherches exactes
- L'**espace mémoire** est significativement plus élevé pour la Skip-List (niveaux supplémentaires)

---

## Auteur

**Paul Rivaud** — projet réalisé dans le cadre d'un cours d'algorithmique avancée.

