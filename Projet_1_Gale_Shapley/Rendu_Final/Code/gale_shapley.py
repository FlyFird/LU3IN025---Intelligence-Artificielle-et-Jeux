# Partie 1

# Question 3

def gale_shapley_etu(maListeH,maListeF,current_man,current_women,taille_max):
    """
    maListeH -> list*list*str : les preferences des hommes(etudiant)
    maListeF -> list*list*str : les preferences des femmes(master)
    current_man -> list*str : liste des hommes
    current_women -> list*str : liste des femmes
    taille_max -> capacite maximun des preferences des femmes
    
    La fonction applique l algo de gale shapley du cote des etudiants
    
    Return : la solution de gale shapley
    """
    
    couple={}#la solution final de gale shapley
    taille={j: 0 for j in current_women} #dictionnaire sur la capacite actuelle des femmes (master) qui est initialise a 0
    position = {j: 0 for j in current_man} #dictionnaire sur la postion actuelle des preferences des hommes (etudiant) qui est initialise a 0
    agent=[x for x in range(len(current_man))]#la file d attente des hommes(etudiant)
    
    #Debut de l'algo 
    while agent!=[]:
        
        i=agent[0]
        #verifie si l'agent est libre mais theoriquement les agents sont libres
        if current_man[i] not in couple.keys():
            free_man=current_man[i]
            target=maListeH[i][position[free_man]]
            
            #verifie si la target n est pas encore pris ou s il reste de la place
            if (target not in couple.values()) or (taille[target]<int(taille_max[int(target)])):
                couple[free_man]=target
                taille[target]+=1 
                agent.pop(0)
                
            #sinon il va regarder dans les preferences de la femme, pour voir qui est le meilleur pour elle
            else:
                liste_cle=[free_man]
                tmp=couple.copy()
                taille[target]=0
                position[free_man]+=1
                
                #cherche les autres agents qui ont le meme target que lui
                for cle,valeur in couple.items():
                    if target==valeur:
                        liste_cle.append(cle)
                        position[cle]+=1
                        tmp.pop(cle,valeur)
                        agent.append(int(cle))
                        
                #regarde les parametres du target pour garder que ces pref        
                for x in range(len(maListeF[int(target)])):
                    #regarde un par un de la gauche vers la droite, et si la preference est dans la liste de cle alors il ajoute
                    if maListeF[int(target)][x] in liste_cle:
                        tmp[maListeF[int(target)][x]]=target
                        position[maListeF[int(target)][x]]-=1
                        taille[target]+=1
                        agent.remove(int(maListeF[int(target)][x]))
                    if taille[target]>=int(taille_max[int(target)]):#quand la capacite est atteint, il arrete la boucle
                        couple=tmp.copy()
                        break
    return couple


# Question 4

def gale_shapley_spe(maListeH,maListeF,current_man,current_women,taille_max):

    """
    maListeH -> list*list*str : Liste des preferences des hommes(etudiant)
    maListeF -> list*list*str : Liste des preferences des femmes(master)
    current_man -> list*str :   Liste des hommes (etudiant)
    current_women -> list*str : Liste des femmes (master)
    taille_max -> capacite maximun des preferences des femmes (master)

    La fonction applique l'algo de Gale-Shapley du cote des masters

    Return : L'affectation (mariage) produit par Gale-Shapley cote master
    """

    couple={j: [] for j in current_man}#la solution final de gale shapley
    position = {j: 0 for j in current_man}#dictionnaire sur la postion actuelle des preferences des hommes (etudiant) qui est initialise a 0
    agent=[x for x in range(len(current_man))]#la file d attente des hommes(etudiant)

    # Debut de l algo
    while agent != []:
        i = agent[0]        # On recupere le 1er etudiant dans la file qui n'a pas encore propose

        # Verifie si l'agent est libre (mais theoriquement les agents sont libres)
        if couple[current_man[i]] == [] or len(couple[current_man[i]]) < taille_max[i]:
            free_man = current_man[i]
            target = maListeH[i][position[free_man]]

            # Si la target est deja pris par lui meme
            if target in couple[free_man]:
                position[free_man]+=1
                continue

            # Verifie si la target n est pas encore pris
            if not(any(target in liste for liste in couple.values())):
                couple[free_man].append(maListeH[i][position[free_man]])
                # Si la capacite max n'est pas atteint, alors il augmente de 1 la position (passe au suivant)
                if len(couple[current_man[i]])<taille_max[i]:
                    position[free_man]+=1
                # Sinon il retire de la file d attente
                else:
                    agent.pop(0)

            # Sinon il va regarder dans les preferences de la femme, pour voir qui est le meilleur pour elle
            else:
                liste_cle=[free_man]
                tmp=couple.copy()
                position[free_man]+=1

                # Cherche les autres agents qui ont la meme target que lui
                for cle,valeur in couple.items():
                    if target in valeur:
                        liste_cle.append(cle)
                        if (taille_max[int(cle)]-len(tmp[cle])) == 0:   # Cas si il a plusieurs preferences
                            position[cle] += 1
                        tmp[cle].remove(target)
                        if int(cle) not in agent:       # n ajoute pas les cles en double
                            agent.append(int(cle))
                        break

                # Regarde les parametres de target pour garder que ses pref
                for x in range(len(maListeF[int(target)])):
                    # Regarde un par un de la gauche vers la droite, et si la preference est dans la liste de cle alors il ajoute
                    if maListeF[int(target)][x] in liste_cle:
                        tmp[maListeF[int(target)][x]].append(target)
                        position[maListeF[int(target)][x]] -= 1
                        # Quand la capacite est atteint, il arrete la boucle
                        if len(couple[maListeF[int(target)][x]]) >= taille_max[int(maListeF[int(target)][x])]:
                            agent.remove(int(maListeF[int(target)][x]))
                        break
                couple = tmp.copy()
    return couple