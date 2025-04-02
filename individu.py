import random

#Classe representant un individu d'une popoulation (algo genetique)

class Individu:

    #initialise les champs privés
    def __var(self):
        self.geno = [] #genotype (geno[a] = la touche attribuee à la lettre A)
        self.fitness = 0 #fitness de l'individu
        self.droite = {} #liste des touches de la partie droite du clavier
        self.gauche = {} #liste des touches de la prtie gauche du clavier

    #Constructeur de la classe
    def __init__(self, geno=[]):
        self.__var()
        if len(geno) != 26: #si le genotype n'est pas valide ou vide
            self.__random_geno() #genotype aleatoire
        else:
            self.geno = geno
        self.trierDG()

    #Génère un genotype aléatoire
    def __random_geno(self):
        rand = random.sample(range(40), 26)
        for n in rand:
            self.geno.append(n)

    #Tri les touches du clavier en fonction de leur position
    def trierDG(self):
        for i in range(26):
            lettre = chr(i+97)
            touche = self.geno[i]
            if touche > 19 :
                self.droite[lettre] = touche
            else:
                self.gauche[lettre] = touche

    #Evaluation de la fitness de l'individu sous hypothese de 2 mains
    def evaluation_2mains(self, bigramme):
        if len(self.geno) != 26:
            self.fitness = 0
            return
        for g in self.gauche:
            for d in self.droite:
                self.fitness += float(bigramme[ord(g)-97][ord(d)-97])
        for d in self.droite:
            for g in self.gauche:
                self.fitness += float(bigramme[ord(d)-97][ord(g)-97])
        self.evaluation_1main(bigramme)
        self.fitness = round(self.fitness,2)

    
    def evaluation_1main(self, bigramme):
        if len(self.geno) != 26:
            self.fitness = 0
            return
        for i in range(40):
            if i in self.geno:
                index = self.geno.index(i)
                neighbour = [index-5, index-4, index-3, index-1, index+1, index+3, index+4, index+5] #8 voisins de la touche
                for n in neighbour:
                    if n >= 0 and n < 40:
                        try:
                            n_value = self.geno.index(n)
                            self.fitness += float(bigramme[index][n_value])
                        except:
                            pass


    def print_as_keyboard(self):
        print("_"*20)
        for i in range(40):
            if i in self.geno:
                print("|"+chr(self.geno.index(i)+65), end="")
            else:
                print("| ", end="")
            if i%10 == 9:
                print("|")
        print("_"*20)
        print("  GAUCHE  ^  DROITE\n          |")

    #Affichage de l'individu (utiliser par print)
    def __str__(self):
        s = "Individu: "
        for i in range(26):
            s += chr(i+97) + ":" + str(self.geno[i]) + " | "
        return s+str(f'\nfitness: {round(self.fitness,2)}\n Gauche: {self.gauche}\n Droite: {self.droite}\n')