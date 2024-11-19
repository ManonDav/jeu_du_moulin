from pion import *
from jeu import *
from niveau import *
import random

#coordonnées des cases disponibles du plateau
COORD=[(100,20),(400,20),(700,20),
       (200,100),(400,100),(600,100),
       (300,180),(400,180),(500,180),
       (100,250),(200,250),(300,250),(500,250),(600,250),(700,250),
       (300,320),(400,320),(500,320),
       (200,400),(400,400),(600,400),
       (100,480),(400,480),(700,480)]

#coordonnées matricielle des cases disponibles du plateau
COORD_MAT=[(0,0),(0,3),(0,6),
           (1,1),(1,3),(1,5),
           (2,2),(2,3),(2,4),
           (3,0),(3,1),(3,2),(3,4),(3,5),(3,6),
           (4,2),(4,3),(4,4),
           (5,1),(5,3),(5,5),
           (6,0),(6,3),(6,6)]

def init_joueur():
    """
        Initialise un joueur
    """
    joueur={}
    joueur["liste_pion"]=[]
    joueur["nb_pion"]=0
    joueur["direction"]=None
    joueur["moulin"]=[]
    joueur["pion_place"]=0
    return joueur
    
def ajoute_pion_liste(joueur,pion):
    """
        dico, dico =>
        Ajoute un pion aux pions de joueur
    """
    joueur["liste_pion"].append(pion)
    joueur["nb_pion"]+=1
    joueur["pion_place"]+=1
    
def retirer_pion(joueur,pion,plateau):
    """
        dico, dico, dico =>
        Retire un pion de joueur et met à jour la matrice
    """
    n_liste=[]
    stock=0
    liste=joueur["liste_pion"]
    for i in range(len(liste)):
        if liste[i]!=pion:
            n_liste.append(liste[i])
        else:
            stock=pion["coord_mat"]
    joueur["liste_pion"]=n_liste
    joueur["nb_pion"]-=1
    plateau["état"][stock[0]][stock[1]]=0
    
def dessiner_pions_joueurs(l):
    """
        liste_pion =>
        Dessine les pions du joueur sur le plateau
    """
    for i in range(len(l)):
        pion_dessine(l[i])
        
def est_dans_liste_pion(liste,pion):
    """
        liste_pion, pion => Bool
        Teste si un pion est dans la liste de pion
    """
    for i in range(len(liste)):
        if pion["x"]==liste[i]["x"] and pion["y"]==liste[i]["y"]:
            return True
    return False


def trouver_pion(liste,pion):
    """
        liste_pion , pion => pion
        Trouve le pion dans la liste et le retourne
    """
    for i in range(len(liste)):
        if pion["x"]==liste[i]["x"] and pion["y"]==liste[i]["y"]:
            return liste[i]

def trouver_pion_correspondant(liste,position):
    """
        liste_pion, (int,int) =>
        - position appartient à COORD
        Trouve le pion qui a les coordonnées position et le retourne
    """
    for i in range(len(liste)):
        x_ok=False
        y_ok=False
        for j in range(-15,15):
            if position[0]==liste[i]["position"][0]+j:
                x_ok=True
            if position[1]==liste[i]["position"][1]+j:
                y_ok=True
            if x_ok and y_ok:
                return liste[i]
    return None

""" Moulin """

def pion_moulin_bouger(joueur_pion, liste_moulin):
    """
        liste_pion_joueur, liste_pion_qui_forme_un_moulin =>
        Vérifie si un des pions qui formait un moulin n'a pas bougé si un pion a bougé le moulin n'existe plus donc on l'enlève de la liste moulin
    """
    if len(liste_moulin)>0 and len(liste_moulin[0])>0:
        for i in range(len(liste_moulin)):
            compt=0
            for k in range(len(liste_moulin[0])):
                for j in range(len(joueur_pion)):
                    if liste_moulin[i][k]==joueur_pion[j]["position"]:
                        compt+=1
            if compt<3:
                liste_moulin.pop(i)
                return
    
def test_moulin(liste,joueur):
    """
        liste_pion, dico => Bool
        Teste si le joueur a formé un moulin 
    """
    resultat={}
    liste_gh=[]
    liste_db=[]
    
    for i in range(len(liste)):
        if liste[i]["position"][0]==400:
            if liste[i]["position"][1]<=180:
                liste_gh.append(liste[i]["position"])
            else:
                liste_db.append(liste[i]["position"])
        else:
            if liste[i]["position"][0] in resultat:
                resultat[liste[i]["position"][0]]+=1
            else:
                resultat[liste[i]["position"][0]]=1
                
    for coord,elem in resultat.items():
        if elem==3:
            liste_moulin=[]
            for j in range(len(liste)):
                if liste[j]["position"][0]==coord:
                    liste_moulin.append(liste[j]["position"])
            if liste_moulin not in joueur["moulin"]:
                joueur["moulin"].append(liste_moulin)
                return True

    
    if len(liste_gh)==3 and liste_gh not in joueur["moulin"]:
        joueur["moulin"].append(liste_gh)
        return True
    
    if len(liste_db)==3 and liste_db not in joueur["moulin"]:
        joueur["moulin"].append(liste_db)
        return True
        
    liste_gh=[]
    liste_db=[]
    resultat={}
    
    for j in range(len(liste)):
        if liste[j]["position"][1]==250:
            if liste[j]["position"][0]<=300:
                liste_gh.append(liste[j]["position"])
            else:
                liste_db.append(liste[j]["position"])
        else:
            if liste[j]["position"][1] in resultat:
                resultat[liste[j]["position"][1]]+=1
            else:
                resultat[liste[j]["position"][1]]=1
    
    for coord,elem in resultat.items():
        if elem==3:
            liste_moulin=[]
            for j in range(len(liste)):
                if liste[j]["position"][1]==coord:
                    liste_moulin.append(liste[j]["position"])
            if liste_moulin not in joueur["moulin"]:
                joueur["moulin"].append(liste_moulin)
                return True
    
    if len(liste_gh)==3 and liste_gh not in joueur["moulin"]:
        joueur["moulin"].append(liste_gh)
        return True
    
    if len(liste_db)==3 and liste_db not in joueur["moulin"]:
        joueur["moulin"].append(liste_db)
        return True
    return False

""" Ordinateur """

def init_ordi():
    """
        Initialise l'ordinateur
    """
    ordi={}
    ordi["liste_pion"]=[]
    ordi["nb_pion"]=0
    ordi["direction"]=None
    ordi["moulin"]=[]
    ordi["pion_place"]=0
    return ordi


            
"""Fase 1"""

def choisir_emplacement_ordi(ordi,joueur,niveau,plateau):
    """
        dico_ordi , dico_joueur, dico_niveau, dico_plateau => pion
        Choisi aléatoirement un emplacement disponible puis créer un pion et le retourne
    """
    position_pion=random.randint(0,len(COORD)-1)
    while not(emplacement_disponible(COORD[position_pion], ordi["liste_pion"], joueur["liste_pion"])):
        position_pion=random.randint(0,len(COORD)-1)
    pion=pion_init(niveau["surf"],COORD[position_pion],(119,181,254))
    mettre_a_jour_matrice(plateau,COORD_MAT[position_pion],3)
    return pion

def placer_pion_angle_libre(liste_angle,niveau,plateau):
    """
        liste((int,int)), dico_niveau, dico_plateau => pion
        Choisi un emplacment dans liste_angle puis créer un pion et le retourne
    """
    choix=random.randint(0,len(liste_angle)-1)
    mettre_a_jour_matrice(plateau,liste_angle[choix],3)
    coord=chercher_coord_pygame(liste_angle[choix][0],liste_angle[choix][1])
    pion=pion_init(niveau["surf"],coord,(119,181,254))
    return pion
    
def angle_carre_grand_libre(plateau):
    """
        dico_plateau => liste((int,int))
        Retourne la liste des grandes angles libres
    """
    liste_angle=[]
    if plateau["état"][0][0]==0:
        liste_angle.append((0,0))
    if plateau["état"][0][6]==0:
        liste_angle.append((0,6))
    if plateau["état"][6][0]==0:
        liste_angle.append((6,0))
    if plateau["état"][6][6]==0:
        liste_angle.append((6,6))
    return liste_angle

def angle_carre_moyen_libre(plateau):
    """
        dico_plateau => liste((int,int))
        Retourne la liste des moyens angles libres
    """
    liste_angle=[]
    if plateau["état"][1][1]==0:
        liste_angle.append((1,1))
    if plateau["état"][1][5]==0:
        liste_angle.append((1,5))
    if plateau["état"][5][1]==0:
        liste_angle.append((5,1))
    if plateau["état"][5][5]==0:
        liste_angle.append((5,5))
    return liste_angle

"""Fase 2"""

def choisir_pion(liste):
    """
        liste_pion => pion
        Choisi aléatoirement un pion dans la liste
    """
    i=random.randint(0,len(liste)-1)
    pion=liste[i]
    return pion

def choisir_direction(o,liste_direction):
    """
        dico_ordi, liste(str)
        Cherche aléatoirement une direction dans les directions possibles de liste direction
    """
    if len(liste_direction)>1:
        i=random.randint(0,len(liste_direction)-1)
        o["direction"]=liste_direction[i]
    else:
        o["direction"]=liste_direction[0]
        

""" Possibiltés d'un moulin """

def test_2_pions_alignes(liste):
    """
        liste_pion => liste((int,int)) #contient les coordonnées matricielles
        Teste si 2 pions dans liste sont alignés
    """
    resultat={}
    liste_gh=[]
    liste_db=[]
    liste_resultat=[]
    
    for i in range(len(liste)):
        if liste[i]["position"][0]==400:
            if liste[i]["position"][1]<=180:
                liste_gh.append(liste[i]["coord_mat"])
            else:
                liste_db.append(liste[i]["coord_mat"])
        else:
            if liste[i]["position"][0] in resultat:
                resultat[liste[i]["position"][0]]+=1
            else:
                resultat[liste[i]["position"][0]]=1
    for coord,elem in resultat.items():
        if elem==2:
            liste_2_pions_aligne=[]
            for j in range(len(liste)):
                if liste[j]["position"][0]==coord:
                    liste_2_pions_aligne.append(liste[j]["coord_mat"])
            if liste_2_pions_aligne not in liste_resultat:
                liste_resultat.append(liste_2_pions_aligne)

    
    if len(liste_gh)==2 and liste_gh not in liste_resultat:
        liste_resultat.append(liste_gh)
    
    if len(liste_db)==2 and liste_db not in liste_resultat:
        liste_resultat.append(liste_db)
        
    liste_gh=[]
    liste_db=[]
    resultat={}
    
    for j in range(len(liste)):
        if liste[j]["position"][1]==250:
            if liste[j]["position"][0]<=300:
                liste_gh.append(liste[j]["coord_mat"])
            else:
                liste_db.append(liste[j]["coord_mat"])
        else:
            if liste[j]["position"][1] in resultat:
                resultat[liste[j]["position"][1]]+=1
            else:
                resultat[liste[j]["position"][1]]=1
    
    for coord,elem in resultat.items():
        if elem==2:
            liste_2_pions_aligne=[]
            for j in range(len(liste)):
                if liste[j]["position"][1]==coord:
                    liste_2_pions_aligne.append(liste[j]["coord_mat"])
            if liste_2_pions_aligne not in liste_resultat:
                liste_resultat.append(liste_2_pions_aligne)
    
    if len(liste_gh)==2 and liste_gh not in liste_resultat:
        liste_resultat.append(liste_gh)
        
    
    if len(liste_db)==2 and liste_db not in liste_resultat:
        liste_resultat.append(liste_db)
        
    return liste_resultat


def chercher_coord_manquant(liste_des_possibilites_moulin,liste_pion_joueur,plateau):
    """
        liste((int,int)) # coord_mat, liste_pion, dico_plateau => (int,int), int
        Cherche une coordonnée manquante et vide qui pourrait former un moulin
    """
    for i in range(len(liste_des_possibilites_moulin)):
        coord=trouver_coord_manquante(liste_des_possibilites_moulin[i],plateau)
        if coord != None:
            if coord_libre(coord,liste_pion_joueur):
                return coord,i
    return None,None

def trouver_coord_manquante(liste_2_pions_aligne,plateau):
    """
        liste((int,int)) #coord_mat, dico_plateau => (int,int) #coord_mat
        Trouve la coordonnée manquantes pour former 3 pions alignés
    """
    pion1=liste_2_pions_aligne[0]
    pion2=liste_2_pions_aligne[1]
    if pion1[0]==pion2[0]:
        if pion1[0]==3 and pion1[1]<=2:
            for i in range(3):
                if plateau["état"][pion1[0]][i]==0:
                    return (pion1[0],i)
        elif pion1[0]==3 and pion1[1]>=4:
            for i in range(4,7):
                if plateau["état"][pion1[0]][i]==0:
                    return (pion1[0],i)
        else:
            for i in range(len(plateau["état"][pion1[0]])):
                if plateau["état"][pion1[0]][i]==0:
                    return (pion1[0],i)
    elif pion1[1]==pion2[1]:
        if pion1[1]==3 and pion1[0]<=2:
            for i in range(3):
                if plateau["état"][i][pion1[1]]==0:
                    return (i,pion1[1])
        elif pion1[1]==3 and pion1[0]>=4:
            for i in range(4,7):
                if plateau["état"][i][pion1[1]]==0:
                    return (i,pion1[1])
        else:
            for i in range(len(plateau["état"])):
                if plateau["état"][i][pion1[1]]==0:
                    return (i,pion1[1])

def chercher_3e_pion(liste,liste_des_possibilites_moulin_o):
    """
        liste_pions_joueur, liste((int,int)) => pion
        Retourne le 3e pion pour former un moulin
    """
    for i in range(len(liste)):
        var=False
        for j in range(len(liste_des_possibilites_moulin_o)):
            if liste[i]["coord_mat"]==liste_des_possibilites_moulin_o[j]:
                var=True
        if not(var):
            return liste[i]

def trouver_meilleur_pion_bouger(liste_ordi,plateau,o,liste_adverse_moulin):
    """
        liste_pion, dico_plateau, ordi_dico, liste([(int,int),(int,int),(int,int)]) => dico_pion
        Essaye de trouver le meilleur pion à bouger
    """
    #tous d'abord, on regarde si un pion pourrait former un moulin
    for j in range(len(liste_ordi)):
        liste_direction=chercher_direction_possible(liste_ordi[j],plateau)
        if liste_direction!=[]:
            for i in range(len(liste_direction)):
                o["direction"]=liste_direction[i]
                
                changer_coord(liste_ordi[j],liste_ordi[j]["position"][0],liste_ordi[j]["position"][1],o,plateau,3)
                liste_des_possibilites_moulin=test_2_pions_alignes(o["liste_pion"])
                if test_moulin(o["liste_pion"],o):
                    o["moulin"].pop(-1)
                    return liste_ordi[j]
                else:
                    trouver_direction_inverse(o)
                    changer_coord(liste_ordi[j],liste_ordi[j]["position"][0],liste_ordi[j]["position"][1],o,plateau,3)
                    
    #puis, on regarde si un pion pourrait bloquer un moulin ennemi 
    for k in range(len(liste_ordi)):
        liste_direction=chercher_direction_possible(liste_ordi[k],plateau)
        if liste_direction != []:
            for w in range(len(liste_direction)):
                o["direction"]=liste_direction[w]
                changer_coord(liste_ordi[k],liste_ordi[k]["position"][0],liste_ordi[k]["position"][1],o,plateau,3)
                if permet_de_former_un_moulin(liste_adverse_moulin,liste_ordi[k]):
                    return liste_ordi[k]
                else:
                    trouver_direction_inverse(o)
                    changer_coord(liste_ordi[k],liste_ordi[k]["position"][0],liste_ordi[k]["position"][1],o,plateau,3)
    return None

def trouver_direction_inverse(o):
    """
        dico_ordi =>
        Permet de donner la direction adverse à celle actuelle
    """
    if o["direction"]=="droite":
        o["direction"]="gauche"
    elif o["direction"]=="gauche":
        o["direction"]="droite"
    elif o["direction"]=="bas":
        o["direction"]="haut"
    elif o["direction"]=="haut":
        o["direction"]="bas"

def permet_de_former_un_moulin(liste_moulin,pion_o):
    """
        liste([(int,int)]), dico_pion => Bool
        Teste si le pion_o forme un moulin avec les moulins potentielles
    """
    for i in range(len(liste_moulin)):
        pion_1=liste_moulin[i][0]
        pion_2=liste_moulin[i][1]
        if pion_1!=pion_o["coord_mat"] and pion_2!=pion_o["coord_mat"]:
            if pion_1[0]==pion_2[0] and pion_o["coord_mat"][0]==pion_1[0]:
                if (pion_1[0]==3 and pion_1[1]<=2 and pion_o["coord_mat"][1]>2) or (pion_1[0]==3 and pion_1[1]>=4 and pion_o["coord_mat"][1]<4):
                    return False
                else:
                    return True
            if pion_1[1]==pion_2[1] and pion_o["coord_mat"][1]==pion_1[1]:
                if (pion_1[1]==3 and pion_1[0]<=2 and pion_o["coord_mat"][0]>2) or (pion_1[1]==3 and pion_1[0]>=4 and pion_o["coord_mat"][0]<4):
                    return False
                else:
                    return True
    return False

def choisir_pion_non_moulin(liste_moulin,liste_pion):
    """
        liste([(int,int),(int,int),(int,int)]), liste(dico_pion)=> dico_pion
        Choisir un pion qui ne forme pas un moulin
    """
    pion=choisir_pion(liste_pion)
    while est_dans(liste_moulin,pion):
        pion=choisir_pion(liste_pion)
    return pion

def choisir_pion_moulin(liste_moulin,liste_pion):
    """
        liste([(int,int),(int,int),(int,int)]), liste(dico_pion)=> dico_pion
        Choisir un pion qui forme un moulin
    """
    i=random.randint(0,len(liste_moulin)-1)
    j=random.randint(0,len(liste_moulin[i])-1)
    for k in range(len(liste_pion)):
        if liste_pion[k]["position"]==liste_moulin[i][j]:
            return liste_pion[k]

def est_dans(liste_moulin,pion):
    """
        liste([(int,int),(int,int),(int,int)]), dico_pion => Bool
        Vérifie si pion se trouve dans liste_moulin
    """
    for i in range(len(liste_moulin)):
        for j in range(len(liste_moulin[i])):
            if pion["position"]==liste_moulin[i][j]:
                return True
    return False

""" Fonction pour le joueur et l'ordinateur """
 
def coord_libre(coord,liste_pion_joueur):
    """
        (int,int), liste(dico_pion) => Bool
        Teste si un pion de la liste liste_pion_joueur occupe coord
    """
    for i in range(len(liste_pion_joueur)):
        if liste_pion_joueur[i]["coord_mat"]==coord:
            return False
    return True
                     
def emplacement_disponible(coordonnes,l_ordi,l_joueur):
    """
        (int,int), liste(pion_dico), liste(pion_dico) => Bool
        Teste si les coordonnes ne sont pas déjà pris par un pion
    """
    for i in range(len(l_ordi)):
        if l_ordi[i]["position"][0]==coordonnes[0] and l_ordi[i]["position"][1]==coordonnes[1]:
            return False
    for j in range(len(l_joueur)):
        if l_joueur[j]["x"]==coordonnes[0] and l_joueur[j]["y"]==coordonnes[1]:
            return False
    return True

def verifier_coord(souris_pos,l_ordi,l_joueur):
    """
        (int,int), liste(dico_pion), liste(dico_pion) => Bool
        Trouve les vraies coordonnées de souris_pos puis vérifie qu'elle ne sont pas déjà occupé
    """
    x=souris_pos[0]
    y=souris_pos[1]
    vrai_COORD=0
    for i in range(len(COORD)):
        x_ok=False
        y_ok=False
        for j in range(-15,15):
            if x==COORD[i][0]+j:
                x_ok=True
            if y==COORD[i][1]+j:
                y_ok=True
            if x_ok and y_ok:
                vrai_COORD=COORD[i]
    
    if vrai_COORD!=0:
        for k in range(len(l_ordi)):
            if l_ordi[k]["position"]==vrai_COORD:
                return False
        for l in range(len(l_joueur)):
            if l_joueur[l]["position"]==vrai_COORD:
                return False
        return True
    else:
        return False

def bloquer(liste_joueur,plateau):
    """
        liste_pion, dico_plateau => Bool
        Teste si les pions de liste_joueur peuvent encore bouger
    """
    if len(liste_joueur)>0:
        for i in range(len(liste_joueur)):
            liste_direction=chercher_direction_possible(liste_joueur[i],plateau)
            if len(liste_direction)>0:
                return False
        return True
    return False
