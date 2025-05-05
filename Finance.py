import json
import os
from datetime import datetime

# Fichier pour stocker les données
DATA_FILE = "depenses.json"

def charger_donnees():
    """Charge les données depuis le fichier JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as fichier:
                return json.load(fichier)
        except json.JSONDecodeError:
            print("Erreur lors du chargement du fichier. Création d'une nouvelle base de données.")
            return []
    else:
        return []

def sauvegarder_donnees(depenses):
    """Sauvegarde les données dans un fichier JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as fichier:
        json.dump(depenses, fichier, ensure_ascii=False, indent=4)

def ajouter_depense(depenses):
    """Ajoute une nouvelle dépense à la liste"""
    print("\n=== Ajouter une dépense ===")
    
    try:
        montant = float(input("Montant: "))
        if montant <= 0:
            print("Le montant doit être positif.")
            return
    except ValueError:
        print("Veuillez entrer un montant valide.")
        return
    
    description = input("Description: ")
    if not description.strip():
        print("La description ne peut pas être vide.")
        return
    
    # Liste prédéfinie de catégories
    categories = ["Alimentation", "Transport", "Logement", "Loisirs", "Santé", "Éducation", "Autres"]
    
    print("\nCatégories disponibles:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    try:
        choix = int(input("\nChoisissez une catégorie (numéro): "))
        if 1 <= choix <= len(categories):
            categorie = categories[choix-1]
        else:
            print("Choix invalide. Catégorie définie comme 'Autres'.")
            categorie = "Autres"
    except ValueError:
        print("Entrée invalide. Catégorie définie comme 'Autres'.")
        categorie = "Autres"
    
    # Création du dictionnaire pour la dépense
    date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nouvelle_depense = {
        "id": len(depenses) + 1,
        "montant": montant,
        "description": description,
        "categorie": categorie,
        "date": date_actuelle
    }
    
    depenses.append(nouvelle_depense)
    sauvegarder_donnees(depenses)
    print(f"Dépense de {montant} DH ajoutée avec succès dans la catégorie '{categorie}'.")

def afficher_depenses(depenses):
    """Affiche toutes les dépenses"""
    if not depenses:
        print("\nAucune dépense enregistrée.")
        return
    
    print("\n=== Historique des dépenses ===")
    print(f"{'ID':<4} {'Date':<20} {'Montant':<10} {'Catégorie':<15} {'Description'}")
    print("-" * 70)
    
    for depense in depenses:
        print(f"{depense['id']:<4} {depense['date']:<20} {depense['montant']:<10.2f} {depense['categorie']:<15} {depense['description']}")
    
    # Calcul du total
    total = sum(depense['montant'] for depense in depenses)
    print("-" * 70)
    print(f"Total: {total:.2f} DH")

def afficher_par_categorie(depenses):
    """Affiche les dépenses regroupées par catégorie"""
    if not depenses:
        print("\nAucune dépense enregistrée.")
        return
    
    # Création d'un dictionnaire pour regrouper les dépenses par catégorie
    depenses_par_categorie = {}
    
    for depense in depenses:
        categorie = depense['categorie']
        if categorie not in depenses_par_categorie:
            depenses_par_categorie[categorie] = []
        depenses_par_categorie[categorie].append(depense)
    
    print("\n=== Dépenses par catégorie ===")
    for categorie, liste_depenses in depenses_par_categorie.items():
        total_categorie = sum(dep['montant'] for dep in liste_depenses)
        print(f"\n{categorie} - Total: {total_categorie:.2f} DH")
        print(f"{'ID':<4} {'Date':<20} {'Montant':<10} {'Description'}")
        print("-" * 60)
        
        for depense in liste_depenses:
            print(f"{depense['id']:<4} {depense['date']:<20} {depense['montant']:<10.2f} {depense['description']}")

def supprimer_depense(depenses):
    """Supprime une dépense par son ID"""
    if not depenses:
        print("\nAucune dépense à supprimer.")
        return depenses
    
    afficher_depenses(depenses)
    
    try:
        id_a_supprimer = int(input("\nEntrez l'ID de la dépense à supprimer (0 pour annuler): "))
        if id_a_supprimer == 0:
            print("Suppression annulée.")
            return depenses
            
        # Recherche de la dépense à supprimer
        for i, depense in enumerate(depenses):
            if depense['id'] == id_a_supprimer:
                depense_supprimee = depenses.pop(i)
                print(f"Dépense '{depense_supprimee['description']}' de {depense_supprimee['montant']} DH supprimée.")
                
                # Réindexation des IDs pour maintenir la cohérence
                for j in range(i, len(depenses)):
                    depenses[j]['id'] = j + 1
                
                sauvegarder_donnees(depenses)
                return depenses
        
        print(f"Aucune dépense trouvée avec l'ID {id_a_supprimer}.")
    except ValueError:
        print("Veuillez entrer un ID valide.")
    
    return depenses

def afficher_statistiques(depenses):
    """Affiche des statistiques simples sur les dépenses"""
    if not depenses:
        print("\nAucune dépense enregistrée pour calculer des statistiques.")
        return
    
    # Calcul des statistiques
    total = sum(depense['montant'] for depense in depenses)
    moyenne = total / len(depenses) if depenses else 0
    
    # Dépense par catégorie
    depenses_par_categorie = {}
    for depense in depenses:
        categorie = depense['categorie']
        if categorie not in depenses_par_categorie:
            depenses_par_categorie[categorie] = 0
        depenses_par_categorie[categorie] += depense['montant']
    
    # Affichage des statistiques
    print("\n=== Statistiques ===")
    print(f"Nombre total de dépenses: {len(depenses)}")
    print(f"Montant total dépensé: {total:.2f} DH")
    print(f"Dépense moyenne: {moyenne:.2f} DH")
    
    print("\nDépenses par catégorie:")
    for categorie, montant in depenses_par_categorie.items():
        pourcentage = (montant / total) * 100 if total > 0 else 0
        print(f"{categorie}: {montant:.2f} DH ({pourcentage:.1f}%)")

def menu_principal():
    """Affiche le menu principal et gère les choix de l'utilisateur"""
    depenses = charger_donnees()
    
    while True:
        print("\n=== GESTIONNAIRE DE FINANCES PERSONNELLES ===")
        print("1. Ajouter une dépense")
        print("2. Afficher toutes les dépenses")
        print("3. Afficher les dépenses par catégorie")
        print("4. Supprimer une dépense")
        print("5. Afficher les statistiques")
        print("0. Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            ajouter_depense(depenses)
        elif choix == "2":
            afficher_depenses(depenses)
        elif choix == "3":
            afficher_par_categorie(depenses)
        elif choix == "4":
            depenses = supprimer_depense(depenses)
        elif choix == "5":
            afficher_statistiques(depenses)
        elif choix == "0":
            print("Merci d'avoir utilisé le gestionnaire de finances personnelles!")
            break
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu_principal()