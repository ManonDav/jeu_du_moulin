from pion import *

def init_plateau(joueur):
    """
        int => dico
        Initialise un plateau
    """
    plateau={}
    plateau["état"]=[[0,1,1,0,1,1,0],
                     [1,0,1,0,1,0,1],
                     [1,1,0,0,0,1,1],
                     [0,0,0,1,0,0,0],
                     [1,1,0,0,0,1,1],
                     [1,0,1,0,1,0,1],
                     [0,1,1,0,1,1,0]]
    plateau["fase"]=0
    plateau["joueur_courant"]=joueur
    return plateau
    

def changer_joueur_courant(plateau,joueur):
    """
        dico, int =>
        Change le joueur courant
    """
    plateau["joueur_courant"]=joueur
    
def changer_fase(plateau):
    """
        dico =>
        Augmente la fase de 1
    """
    plateau["fase"]+=1
    
def mettre_a_jour_matrice(plateau,coord,joueur):
    """
        dico, (int,int), int =>
        Met à jour la matrice aux coord avec un pion appartenant à joueur
    """
    plateau["état"][coord[0]][coord[1]]=joueur
    
def affiche_plateau(plateau):
    """
        dico =>
        Affiche plateau
    """
    for i in range(0,len(plateau)):
        ligne="|"
        for j in range(0,len(plateau[i])):
            if plateau[i][j]==0:
                ligne+="_"
            if plateau[i][j]==1:
                ligne+="-"
            if plateau[i][j]==2:
                ligne+="x"
            if plateau[i][j]==3:
                ligne+="o"
        print(str(i)+ligne+"| \n")

