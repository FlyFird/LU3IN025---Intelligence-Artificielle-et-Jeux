# Partie 1

# Question 6

def paire_instable(affectation, matrix_pref_etu, matrix_pref_spe):
    """
    affectation -> dict*list*str : Affectation (mariage parcours : etudiant)
    matrix_pref_etu -> list*list*str : Liste des preferences des hommes (master)
    matrix_pref_spe -> list*list*str : Liste des preferences des femmes (master)

    Return : Liste des paires instables dans l'affectation
    """

    liste_paires_instables = []

    # On parcourt tous les parcours et les étudiants affectés
    for parcours1, liste_etudiants in affectation.items():
        for etudiant in liste_etudiants:
            liste_pref_etu = matrix_pref_etu[int(etudiant)]

            # Récupérer l'indice du parcours actuel dans les préférences de l'étudiant
            ind_etu_pref1 = liste_pref_etu.index(parcours1)

            # Comparer parcours1 avec tous les autres parcours possibles
            for parcours2 in affectation.keys():
                if parcours2 != parcours1:
                    ind_etu_pref2 = liste_pref_etu.index(parcours2)

                    # Si l'étudiant préfère parcours2 à parcours1
                    if ind_etu_pref2 < ind_etu_pref1:
                        liste_pref_parcours = matrix_pref_spe[int(parcours2)]

                        # Vérifier si parcours2 préfère aussi cet étudiant à ses affectés
                        for etudiant_affecte in affectation[parcours2]:
                            ind_etu_parcours2 = liste_pref_parcours.index(etudiant)
                            ind_etu_affecte_parcours2 = liste_pref_parcours.index(etudiant_affecte)

                            # Si parcours2 préfère l'étudiant à un de ses actuels affectés
                            if ind_etu_parcours2 < ind_etu_affecte_parcours2:
                                if (not((parcours2, etudiant) in liste_paires_instables)):
                                    liste_paires_instables.append((parcours2, etudiant))

    return liste_paires_instables