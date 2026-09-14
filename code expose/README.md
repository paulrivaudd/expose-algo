# Prototype de base de données — Skip-List vs Red-Black Tree

> Implémentation et comparaison de performances de deux structures de données ordonnées appliquées à un moteur de requêtes sur un dataset réel (UCI Adult Census, 32 561 entrées).

---

## Contexte

Ce projet explore deux structures de données classiques en algorithmique pour implémenter un moteur de base de données minimaliste :

- **Skip-List** — structure probabiliste en liste chaînée multi-niveaux. Complexité moyenne O(log n) pour la recherche et l'insertion.
- **Red-Black Tree** — arbre binaire de recherche auto-équilibré. Complexité garantie O(log n) dans le pire cas.

L'objectif est de comparer leurs performances sur des requêtes réelles : recherche exacte, requêtes par plage (range queries), et requêtes filtrées.

---

## Complexités comparées

| Opération         | Skip-List (moy.) | Skip-List (pire) | Red-Black Tree |
|-------------------|------------------|------------------|----------------|
| Recherche         | O(log n)         | O(n)             | O(log n)       |
| Insertion         | O(log n)         | O(n)             | O(log n)       |
| Suppression*      | O(log n)         | O(n)             | O(log n)       |
| Range query       | O(log n + k)     | O(n)             | O(log n + k)   |
| Espace mémoire    | O(n)             | O(n · max_level) | O(n)           |

*k = nombre d'éléments dans l'intervalle.*
*\* Complexité théorique : la suppression n'est pas implémentée dans ce prototype (la base est construite une fois puis interrogée).*

Avec p = 0.5, un nœud de skip-list porte en moyenne 2 pointeurs `forward` : l'espace reste linéaire, mais avec une constante plus élevée que le RB-tree (qui a toujours 3 pointeurs par nœud).

---

## Dataset

**UCI Adult Census Income** (`adult_train.csv`) — 32 561 entrées représentant des individus avec attributs : âge, profession, niveau d'éducation, revenu (>50K / ≤50K).

```
age, workclass, fnlwgt, education, education_num, marital_status,
occupation, relationship, race, sex, capital_gain, capital_loss,
hours_per_week, native_country, class
```

---

## Requêtes implémentées

```python
db.find_by_id(id)                          # Recherche exacte par identifiant
db.find_by_age(age)                        # Toutes les personnes d'un âge donné
db.find_by_age_range(a, b)                 # Range query sur l'âge
db.count_high_income_in_age_range(a, b)    # Range query + filtre sur le revenu
db.average_hours_in_age_range(a, b)        # Range query + agrégat (moyenne)
```

---

## Structure du projet

```
expose-algo/
└── code expose/
    ├── skiplist.py       # Implémentation de la skip-list
    ├── rbtree.py         # Implémentation de l'arbre rouge-noir
    ├── database.py       # Abstraction "base de données" (skip-list ou RBT)
    ├── data_loader.py    # Chargement du CSV, modèle Person
    ├── compare_perf.py   # Benchmarks et mesures de performance
    ├── main.py           # Point d'entrée — démo des requêtes + benchmark
    └── adult_train.csv   # Dataset UCI Adult Census
```

---

## Lancer le projet

Python 3.10+ requis, aucune dépendance externe.

```bash
# Cloner le repo
git clone https://github.com/paulrivaudd/expose-algo.git
cd "expose-algo/code expose"

# Démo des requêtes + benchmark
python main.py adult_train.csv

# Benchmark seul
python compare_perf.py adult_train.csv
```

> Le dataset peut aussi être téléchargé ici : [UCI Adult Census](https://github.com/selva86/datasets/blob/master/adult_train.csv)

---

## Protocole de mesure

Pour chaque taille (1 000, 5 000, 10 000 et 32 561 lignes), `compare_perf.py` mesure :

- **build** — insertion de toutes les personnes, indexées par âge ;
- **search age** — 1 000 recherches exactes sur l'âge (clé avec beaucoup de doublons) ;
- **search id** — 1 000 recherches exactes sur l'identifiant (clé unique) ;
- **range** — 100 range queries sur des intervalles d'âge aléatoires.

La graine aléatoire est fixée (`seed=42`) pour rendre les mesures reproductibles.

---

## Résultats

Exemple de mesures sur le dataset complet (n = 32 561, CPython 3.14 — les valeurs absolues varient selon la machine) :

| Structure      | build (s) | search age (ms) | search id (ms) | range (ms) | équilibrage        |
|----------------|-----------|-----------------|----------------|------------|--------------------|
| SkipList       | 0.056     | 1.11            | 1.22           | 10.8       | niveau max 14 / 20 |
| RedBlackTree   | 0.037     | 0.17            | 0.91           | 37.5       | h = 23, bh = 12    |

Points clés observés :

- **Construction** — le RB-tree est ~1.5× plus rapide : au plus 2 rotations par insertion, et pas de tirage aléatoire.
- **Recherche exacte** — le RB-tree gagne, mais l'écart dépend fortement de la clé :
  - sur l'**âge** (~73 valeurs distinctes pour 32 561 lignes), il est ~6× plus rapide, car il s'arrête dès qu'il rencontre un nœud de même clé, souvent près de la racine, alors que la skip-list descend toujours jusqu'au niveau 0 ;
  - sur l'**id** (clé unique), l'écart tombe à ~1.3× — c'est la comparaison la plus représentative du coût réel d'une descente en O(log n).
- **Range queries** — la **skip-list** est ~3× plus rapide : une fois le début de l'intervalle trouvé, elle suit simplement le niveau 0 (liste chaînée triée), alors que le RB-tree fait un parcours infixe récursif, coûteux en appels de fonctions Python.
- **Équilibrage** — la théorie est vérifiée : niveau max de la skip-list 14 ≈ log₂(32 561) ≈ 15, hauteur du RB-tree 23 ≤ 2·log₂(n+1) ≈ 30.

**Conclusion** : pas de gagnant universel. La skip-list convient aux charges dominées par les range queries (et est plus simple à implémenter) ; le RB-tree offre des recherches exactes plus rapides et des garanties de pire cas déterministes.

---

## Auteur

**Paul Rivaud** — projet réalisé dans le cadre d'un cours d'algorithmique avancée.
