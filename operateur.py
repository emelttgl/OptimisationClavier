#Bibliothèque implémentant différents opérateurs de l'algorithme génétique
#comme la mutation, le croisement, la sélection, etc.

import random

def select_t(inds, n):
    """Tournois: selectionne n individus parmi la liste fournie"""
    maxi = [] #liste des meilleurs individus
    mini = -1 #fitness du moins bon des meilleurs individus
    for i in inds:
        #compare puis stocke les n meiileurs individus
        if len(maxi) < n:
            maxi.append(i)
            if i.fitness < mini or mini == -1:
                mini = i.fitness
        else:
            if i.fitness > mini:
                rmv = "" #individu a supprimer
                tmp = mini #stocke le minimum
                maxi.append(i) #ajoute le nouvel individu
                mini = i.fitness #mets a jour le minimum avec le nouvel individu
                for j in maxi:
                    if j.fitness == tmp:
                        rmv = j #supprime le moins bon des meilleurs individus
                    elif j.fitness < mini: #mets a jour le minimum
                        mini = j.fitness
                maxi.remove(rmv)
    return maxi


def tournois2(inds): 
    """Tournois: selectionne 2 individus parmi la liste fournie"""
    if len(inds) < 2:
        return None, None
    parent = select_t(inds, 2)
    return parent[0], parent[1]


def pxm(ind1, ind2):
    """
    Croisement: croise les deux individus
    :param ind1: parent1
    :param ind2: parent2
    :return: legénotype des deux enfants
    """
    #choisit un point de croisement
    cut1 = random.randint(0, 24) #point de coupe 1
    cut2 = random.randint(cut1 + 1, 25) #point de coupe 2

    enf1 = ind1.geno.copy() #enfant 1
    enf2 = ind2.geno.copy() #enfant 2

    #croise les deux individus
    for i in range(cut1, cut2+1):
        enf1[i] = ind2.geno[i]
        enf2[i] = ind1.geno[i]

    #verifier les permutations
    for j in range(26):
        if j < cut1 or j > cut2:
            enf1 = keep_permu(enf1, enf2, j)
            enf2 = keep_permu(enf2, enf1, j)
    
    return enf1, enf2


def keep_permu(enf1, enf2, i):
    """
    Verifie si le genotype enf1 est une permutation
    :param enf1: genotype d'un enfant
    :param par: genotype d'un parent
    """
    perm = False

    while not perm:
        perm = True
        for j in range(len(enf1)):
            if i != j and enf1[i] == enf1[j]:
                enf1[i] = enf2[j]
                perm = False
                break        
    return enf1


def mutation_remp(ind):
    """
    Mutation: remplace la valuer d'un gène par une autre
    :param ind: genotype d'un individu
    :return: le nouveau genotype
    """
    alea = random.randint(0, 100)

    #2% de chance de muter
    if alea < 2: 
        #index du gène a muter
        mut = random.randint(0, 25)
        #choisit une nouvelle valeur pour le gène
        val = random.randint(0, 39)

        pres = False #valeur deja presente dans le genotype
        for i in range(len(ind)):
            if ind[i] == val and i != mut: #si la valeur est deja presente
                ind[i] = ind[mut] #remplace la valeur par la valeur du gène muté
                ind[mut] = val
                pres = True
                break
        
        if not pres:
            ind[mut] = val
    return ind


def remplacement_t2(inds, enfants):
    """
    Remplacement: forme des groupe de 2 individus + 1 enfant et supprime le moins performant
    :param inds: liste des individus
    :param enfants: liste des enfants
    :return: la nouvelle liste des individus
    """
    random.shuffle(inds) #melange la liste des individus
    random.shuffle(enfants) #melange la liste des enfants
    final = [] #liste finale des individus
    
    while len(inds) != 0:
        r_ind = random.sample(range(len(inds)), 2) #choisit 2 individus au hasard
        r_enf = random.sample(range(len(enfants)), 1) #choisit 1 enfant au hasard
        #ajoute les 3 individus dans une liste
        i1 = inds[r_ind[0]]
        i2 = inds[r_ind[1]]
        poule = [i1, i2, enfants[r_enf[0]]]

        inds.remove(i1) #supprime les individus de la liste
        inds.remove(i2)
        enfants.remove(enfants[r_enf[0]])

        #tournois
        f1, f2 = tournois2(poule)
        final.append(f1)
        final.append(f2)
    return final
