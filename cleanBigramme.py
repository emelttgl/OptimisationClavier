import sys

#Récupération des paramètres
args = sys.argv
if len(args) != 2:
    print("Usage: python3 cleanBigramme.py <file>")
    exit(-1)

#Création d'une liste de 26 par 26
tab = [[0 for i in range(26)] for j in range(26)]

ligne = -1
total = 0;

with open('freqBigrammes.txt', 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('\t')
        if ligne != -1:
            for col in range(1,len(line)):
                # On ajoute la valeur dans la matrice (col-1 car la première colonne ne doit pas être prise en compte)
                tab[ligne][col-1] = float(line[col]) # On convertit la valeur en entier
                # On ajoute la valeur au total
                total += float(line[col])
        ligne += 1

# On divise chaque valeur par le total (pour avoir des %)
for i in range(26):
    for j in range(26):
        tab[i][j] = round(float(tab[i][j] / total)*10000,2)

# Création d'une liste contenant les lettres de l'alphabet
alphabet = [chr(i) for i in range(ord('A'), ord('Z')+1)]

with open('PrctBigramme.txt', 'w') as f:
    for i in range(26):
        for j in range(26):
            f.write(str(tab[i][j]) + ';')
        f.write('\n')

exit(0)