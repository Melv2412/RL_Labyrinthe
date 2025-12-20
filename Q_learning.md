# Q‑learning — Explication algorithmique et fonction mathématique

Ce document explique de manière détaillée l'algorithme Q‑learning, la formule mathématique d'actualisation, les choix de paramètres et les implications pratiques pour un problème de labyrinthe.

## 1. Contexte (MDP)

- Un problème de décision séquentielle est modélisé par un processus de décision markovien (MDP) défini par l'ensemble des états $S$, l'ensemble des actions $A$, la fonction de transition $P(s'\mid s,a)$ et la fonction de récompense $R(s,a,s')$.
- Objectif: apprendre une politique $\\pi(a\mid s)$ qui maximise la somme des récompenses cumulées (retour) espérées.

## 2. Table de valeurs Q

- Q‑learning stocke une table $Q(s,a)$ qui estime la valeur (gain attendu) de prendre l'action $a$ dans l'état $s$ puis agir de façon optimale ensuite.
- Dans les petits environnements (comme un labyrinthe discret), on utilise une Q‑table tabulaire de taille $|S|\times|A|$.

## 3. Règle d'actualisation (formule)

À chaque transition observée $(s,a,r,s')$, on met à jour $Q(s,a)$ selon la règle:

$$
Q(s,a) \leftarrow Q(s,a) + \alpha \bigl(r + \gamma \max_{a'} Q(s',a') - Q(s,a)\bigr)
$$

Où:
- $\alpha$ est le taux d'apprentissage (learning rate), $0<\alpha\le 1$.
- $\gamma$ est le facteur d'actualisation (discount factor), $0\le\gamma<1$.
- $r$ est la récompense immédiate reçue après avoir pris $a$ en $s$ et atteint $s'$.

Interprétation mathématique:
- L'erreur temporelle (TD error) est $\delta = r + \gamma \max_{a'} Q(s',a') - Q(s,a)$.
- L'actualisation réalise une mise à jour de gradient stochastique vers la cible $r + \gamma \max_{a'} Q(s',a')$.

## 4. Politique d'exploration/exploitation

- Epsilon‑greedy: avec probabilité $\varepsilon$ choisir une action aléatoire (exploration), sinon choisir l'action $\arg\max_a Q(s,a)$ (exploitation).
- Décroissance de $\varepsilon$: on réduit $\varepsilon$ au fil des épisodes (par ex. $\varepsilon_{t+1} = \varepsilon_t \cdot$ decay ou $\varepsilon_{min} + (\varepsilon_0-\varepsilon_{min})\exp(-kt)$).

## 5. Initialisation et paramètres

- Initialiser $Q(s,a)$ à 0 ou à des petites valeurs aléatoires.
- Choix typiques:
  - $\alpha$: 0.1 — 0.5 selon la variance des récompenses.
  - $\gamma$: 0.9 — 0.99 pour valoriser les récompenses futures.
  - $\varepsilon_0$: 0.1 — 1.0 (souvent 1.0 puis décroissance).

## 6. Pseudocode (tabulaire)

1. Initialiser $Q(s,a)$ pour tous $s,a$.
2. Pour épisode = 1..N:
   - initialiser $s$ (position de départ)
   - pour chaque pas de temps jusqu'à terminaison:
     - choisir $a$ selon epsilon‑greedy($Q(s,\cdot)$)
     - exécuter $a$, observer $r,s'$
     - $Q(s,a) \leftarrow Q(s,a) + \alpha (r + \gamma \max_{a'} Q(s',a') - Q(s,a))$
     - $s \leftarrow s'$

## 7. Convergence et garanties

- Pour des tables finies, si chaque paire $(s,a)$ est visitée infiniment souvent et si $\sum_t \alpha_t = \infty$, $\sum_t \alpha_t^2 < \infty$, alors Q‑learning converge vers $Q^*$ (politique optimale) sous hypothèses.
- En pratique, utiliser des décroissances adaptées et s'assurer d'une exploration suffisante.

## 8. Limitations

- État discret requis (tabulaire). Pour grands espaces d'états, on préfère l'approximation par réseau de neurones (Deep Q‑Learning).
- Sensible au design des récompenses (shaping) — mauvaise récompense → politique non désirée.

## 9. Recommandations pour le labyrinthe

- Récompenses: goal = +1 ou +100, step = -0.01 (pour encourager solutions courtes), collision/mur = -0.1.
- Utiliser $\gamma$ proche de 0.95, $\alpha$ entre 0.1 et 0.3, $\varepsilon$ débutant à 1.0 puis décroissant vers 0.05.
- Sauvegarder la Q‑table régulièrement et évaluer sur épisodes sans exploration ($\varepsilon=0$).

---

Pour plus d'exemples pratiques, voir le code dans le dossier `rl_engine` du projet.
