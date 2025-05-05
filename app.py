
categories = ["Alimentation", "Transport", "Logement", "Loisirs", "Autre"]
descriptions = ["Repas", "Course", "Déplacement", "Divertissement", "Autre"]
liste_depenses = []
def afficher_liste(liste):
    for i, element in enumerate(liste, 1):
        print(f"{i}. {element}")

def ajouter_depense():
    montant = input("Entrez le montant de la dépense : ")

    print("\nCatégories :")
    afficher_liste(categories)
    numero_categorie = int(input("Choisissez le numéro de la catégorie : "))
    categorie = categories[numero_categorie - 1]

    print("\nDescriptions :")
    afficher_liste(descriptions)
    numero_description = int(input("Choisissez le numéro de la description : "))
    description = descriptions[numero_description - 1]

    depense = {
        "montant": montant,
        "categorie": categorie,
        "description": description
    }
    liste_depenses.append(depense)
    print("\n Dépense ajoutée avec succès.")
def afficher_depenses():
    if not liste_depenses:
        print("\nAucune dépense enregistrée.")
    else:
        print("\n--- Liste des Dépenses ---")
        for i, dep in enumerate(liste_depenses, 1):
            print(f"{i}. {dep['montant']} DH - {dep['categorie']} - {dep['description']}")
def modifier_depense():
    afficher_depenses()
    if liste_depenses:
        choix = int(input("\nEntrez le numéro de la dépense à modifier : "))
        if 1 <= choix <= len(liste_depenses):
            depense = liste_depenses[choix - 1]
            print("\nLaissez vide pour garder la valeur actuelle.")
            montant = input(f"Montant actuel ({depense['montant']} DH) : ") or depense['montant']

            print("\nCatégories :")
            afficher_liste(categories)
            categorie_input = input(f"Numéro catégorie actuelle ({depense['categorie']}) : ")
            if categorie_input:
                categorie = categories[int(categorie_input) - 1]
            else:
                categorie = depense['categorie']

            print("\nDescriptions :")
            afficher_liste(descriptions)
            description_input = input(f"Numéro description actuelle ({depense['description']}) : ")
            if description_input:
                description = descriptions[int(description_input) - 1]
            else:
                description = depense['description']

            liste_depenses[choix - 1] = {
                "montant": montant,
                "categorie": categorie,
                "description": description
            }
            print("\n Dépense modifiée avec succès.")
        else:
            print("Numéro invalide.")

def supprimer_depense():
    afficher_depenses()
    if liste_depenses:
        choix = int(input("\nEntrez le numéro de la dépense à supprimer : "))
        if 1 <= choix <= len(liste_depenses):
            dep_supprimee = liste_depenses.pop(choix - 1)
            print(f"\n Dépense supprimée : {dep_supprimee['montant']} DH - {dep_supprimee['categorie']} - {dep_supprimee['description']}")
        else:
            print("Numéro invalide.")
def menu():
    while True:
        print("\n=== MENU ===")
        print("1. Ajouter une dépense")
        print("2. Afficher les dépenses")
        print("3. Modifier une dépense")
        print("4. Supprimer une dépense")
        print("5. Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            ajouter_depense()
        elif choix == "2":
            afficher_depenses()
        elif choix == "3":
            modifier_depense()
        elif choix == "4":
            supprimer_depense()
        elif choix == "5":
            print(" Merci d'utiliser notre application!!")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
menu()
