# Démarche d'implémentation

Ce document décrit étape par étape la démarche d'implémentation d'un agent Q‑learning pour un labyrinthe discret. Il couvre la représentation de l'environnement, la conception des récompenses, la mise en œuvre de la boucle d'entraînement, la sauvegarde et l'évaluation.

## 1. Représentation de l'environnement

- Grille discrète: chaque cellule représente un état $s$. Représenter le labyrinthe comme une matrice 2D.
- États spéciaux: départ, but, murs, cases neutres.
- Encodage d'état: on peut utiliser un index unique par cellule (ex: `state_id = y * width + x`) ou un tuple `(x,y)`.

## 2. Actions

- Ensemble d'actions typique: `['UP','DOWN','LEFT','RIGHT']`.
- À chaque action, définir la transition: si l'action mène à un mur, soit rester sur place (et donner une petite pénalité), soit ignorer l'action.

## 3. Conception des récompenses

- Récompense positive pour atteindre la sortie (ex: +1 ou +100).
- Petite pénalité par pas (ex: -0.01) pour favoriser des trajectoires courtes.
- Pénalité pour collision / action invalide (ex: -0.1) si souhaité.

## 4. Structure de la Q‑table

- Mise en place d'une matrice NumPy ou d'un dictionnaire Python: `Q = np.zeros((n_states, n_actions))`.
- Indexation cohérente: avoir des fonctions `state_to_idx(s)` et `action_to_idx(a)`.

## 5. Boucle d'entraînement

Pseudocode simplifié:

```
for episode in range(num_episodes):
    s = env.reset()
    done = False
    while not done:
        a = choose_action_epsilon_greedy(Q, s, eps)
        s2, r, done = env.step(a)
        Q[s,a] += alpha * (r + gamma * np.max(Q[s2,:]) - Q[s,a])
        s = s2
    decay_epsilon()
```

Points pratiques:
- Sauvegarder la Q‑table après N épisodes (pickle ou np.save).
- Enregistrer métriques: récompense par épisode, longueur des épisodes, taux de réussite.

## 6. Politique d'exploration

- Epsilon‑greedy avec décroissance linéaire ou exponentielle.
- Option: utiliser Boltzmann (softmax) si on souhaite exploration basée sur valeurs.

## 7. Évaluation

- Évaluer périodiquement avec $\varepsilon=0$ (policy greedy) sur plusieurs épisodes et calculer la moyenne des récompenses et le taux d'atteinte du but.

## 8. Sauvegarde / Chargement

- Sauvegarder `Q` avec `pickle` ou `numpy.save`:

```
import pickle
with open('q_table.pkl','wb') as f:
    pickle.dump(Q, f)

# Chargement
with open('q_table.pkl','rb') as f:
    Q = pickle.load(f)
```

## 9. Intégration avec l'interface (Django)

- Exposer endpoints pour lancer/arrêter l'entraînement, charger une Q‑table, et exécuter un épisode de démonstration.
- Exemple d'API minimal: `/start_training`, `/stop_training`, `/reset_agent`, `/step_agent`.

## 10. Tests et validation

- Écrire des tests unitaires pour:
  - transitions d'état (env.step)
  - mise à jour Q correcte pour un exemple connu
  - sauvegarde/chargement de Q

## 11. Conseils d'optimisation

- Vectoriser les opérations NumPy quand possible.
- Si l'environnement devient grand, passer à une approximation fonctionnelle (réseau) et utiliser DQN.

---

Cette démarche permet d'implémenter proprement un agent Q‑learning, de le tester et de l'intégrer dans une interface web pour démonstration.
