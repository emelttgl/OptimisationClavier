#Fichier principal du projet
#Ce fichier sert de point de départ pour "simuler un monde" par l'algo génétique

import individu as ind
import subprocess
import operateur as op
import statistics as stat
import random
import argparse
import os

p = argparse.ArgumentParser()
p.add_argument('-t', '--taille', type=int, default=260, help="Taille de la population")
p.add_argument('-f', '--fitness', type=int, default=1, help="Fitness à utililser | 1: 1 main | 2: 2 mains")
arg = p.parse_args()

taille_populations = arg.taille
methode = arg.fitness

with open('PrctBigramme.txt', 'r') as f:
    bigramme = []
    for line in f:
        line = line.strip()
        line = line.split(';')
        bigramme.append(line)

inds = []
enfs = []
nb_gen = 0

#Generation de base
for i in range(taille_populations):
    indi = ind.Individu()
    if methode == 1:
        indi.evaluation_1main(bigramme)
    else:
        indi.evaluation_2mains(bigramme)
    inds.append(indi)
#Recherche du premier elite
for i in inds:
    maxi = 0
    if i.fitness > maxi:
        maxi = i.fitness
        best = i
#print(best.fitness)

cpt = 0
fit_primal = 0

while cpt != 100:
    tmp = inds.copy()
    #selection
    while len(tmp) != 0:
        rand  = random.sample(range(len(tmp)), 4)
        candidats = [tmp[rand[0]], tmp[rand[1]], tmp[rand[2]], tmp[rand[3]]]
        tmp.remove(candidats[0])
        tmp.remove(candidats[1])
        tmp.remove(candidats[2])
        tmp.remove(candidats[3])
        #Selection des parents
        par1, par2 = op.tournois2(candidats)
        #Croisement
        enf1, enf2 = op.pxm(par1, par2)
        #Mutation
        enf1 = op.mutation_remp(enf1)
        enf2 = op.mutation_remp(enf2)
        #Evaluation des enfants
        enf1 = ind.Individu(enf1)
        enf2 = ind.Individu(enf2)
        if methode == 1:
            enf1.evaluation_1main(bigramme)
            enf2.evaluation_1main(bigramme)
        else:
            enf1.evaluation_2mains(bigramme)
            enf2.evaluation_2mains(bigramme)
        #Ajout des enfants a la liste des enfants
        enfs.append(enf1)
        enfs.append(enf2)

    #remplacement de la generation
    inds = op.remplacement_t2(inds, enfs)

    for i in inds:
        maxi = 0
        if i.fitness > maxi:
            maxi = i.fitness
            best = i
    #print(best.fitness)

    m = op.select_t(inds, 10)
    fit = [i.fitness for i in m]
    fit_mean = stat.mean(fit)
    #print(fit_mean)

    if fit_mean < fit_primal-1 or fit_mean > fit_primal+1:
        fit_primal = fit_mean
    else:
        cpt += 1

    #clear console
    subprocess.run(['clear'])
    print(f"Generation: {nb_gen}")
    nb_gen += 1
    
    
print(f"Paramètre utilisé: \n\tTaille de la population: {taille_populations} \n\tMéthode d'évaluation: ", end='')
if methode == 1:
    print("1 main")
else:
    print("2 mains")

print(best)
best.print_as_keyboard()