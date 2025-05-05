# Personal Finance Tracker v1.0

Un système simple de suivi des dépenses personnelles.

## Fonctionnalités

- Ajouter des dépenses (montant, catégorie, description)
- Visualiser l'historique des dépenses
- Consulter le total des dépenses et le nombre d'entrées

## Installation

Aucune installation particulière n'est requise, seulement Python 3.6+ qui est généralement préinstallé sur les systèmes modernes.

## Utilisation

1. Placez les deux fichiers (`finance_tracker.py` et `index.html`) dans le même dossier
2. Lancez le serveur Python:

```
python finance_tracker.py
```

3. Ouvrez votre navigateur web à l'adresse: http://localhost:8000

## Structure de données

Les données sont stockées dans trois listes parallèles:
- `amounts_list` : Liste des montants
- `categories_list` : Liste des catégories
- `descriptions_list` : Liste des descriptions

## Remarques

- Cette version 1.0 est conçue pour la semaine 1 (Bases - Variables & Entrée/Sortie)
- Les données ne sont pas persistantes (elles sont perdues à l'arrêt du serveur)
- Interface simple et intuitive avec HTML/CSS/JavaScript