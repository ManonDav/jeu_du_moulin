import pygame
from jeu import *
import random

COORD=[(100,20),(400,20),(700,20),
       (200,100),(400,100),(600,100),
       (300,180),(400,180),(500,180),
       (100,250),(200,250),(300,250),(500,250),(600,250),(700,250),
       (300,320),(400,320),(500,320),
       (200,400),(400,400),(600,400),
       (100,480),(400,480),(700,480)]

COORD_MAT=[(0,0),(0,3),(0,6),
           (1,1),(1,3),(1,5),
           (2,2),(2,3),(2,4),
           (3,0),(3,1),(3,2),(3,4),(3,5),(3,6),
           (4,2),(4,3),(4,4),
           (5,1),(5,3),(5,5),
           (6,0),(6,3),(6,6)]

def pion_init(niveau,pos,coul):
    """
        dico des éléments de niveau, (int,int), (int,int,int) => rien
        Initialisation du fruit
    """
    pion={}
    pion["niv"]=niveau
    pion["pers"]=2
    pion["nbr"]=9
    pion["couleur"]=coul
    pion["position"]=pos
    pion["x"]=0
    pion["y"]=0
    pion["coord_mat"]=0
    return pion

def valide_coord(pion):
    """
        Dico_pion => Bool
        Vérifie que les coordonées sont possibles
    """
    x=pion["position"][0]
    y=pion["position"][1]
    indice=0
    for j in range(len(COORD)):
        x_ok=False
        y_ok=False
        for i in range(-15,15):
            if x==COORD[j][0]+i:
                x_ok=True
                pion["x"]=COORD[j][0]
            if y==COORD[j][1]+i:
                y_ok=True
                pion["y"]=COORD[j][1]
            if x_ok and y_ok:
                pion["position"]=COORD[j]
                return True
    return False
    
def chercher_coord(point,x,y):
    """
        dico_pion, int ,int => (int,int)
        Renvoie les coordonnées de la matrice qui correspondent aux coordonnées (x,y)
    """
    for i in range(len(COORD)):
        if COORD[i][0]==x and COORD[i][1]==y:
            point["coord_mat"]=COORD_MAT[i]
            
def chercher_coord_pygame(x,y):
    """
        int ,int => (int,int)
        Renvoie les coordonnées qui correspondent aux coordonnées matricielles (x,y) 
    """
    for i in range(len(COORD_MAT)):
        if COORD_MAT[i][0]==x and COORD_MAT[i][1]==y:
            return COORD[i]
            
def changer_coord(point,x,y,j,plateau,nb):
    """
        dico_pion, int ,int , dico_joueur, dico_plateau, int =>
        Change les coordonnées de point 
    """
    if j["direction"]=="gauche" or j["direction"]=="droite":
        for i in range(len(COORD)):
            if COORD[i][0]==x and COORD[i][1]==y:
                if j["direction"]=="gauche":
                    point["position"]=COORD[i-1]
                    point["x"]=point["position"][0]
                    point["y"]=point["position"][1]
                    point["coord_mat"]=COORD_MAT[i-1]
                    plateau["état"][COORD_MAT[i][0]][COORD_MAT[i][1]]=0
                    plateau["état"][COORD_MAT[i-1][0]][COORD_MAT[i-1][1]]=nb
                    
                if j["direction"]=="droite":
                    point["position"]=COORD[i+1]
                    point["x"]=point["position"][0]
                    point["y"]=point["position"][1]
                    point["coord_mat"]=COORD_MAT[i+1]
                    plateau["état"][COORD_MAT[i][0]][COORD_MAT[i][1]]=0
                    plateau["état"][COORD_MAT[i+1][0]][COORD_MAT[i+1][1]]=nb
    
    if j["direction"]=="haut" or j["direction"]=="bas":
        if j["direction"]=="haut":
            plateau["état"][point["coord_mat"][0]][point["coord_mat"][1]]=0
            if point["x"]==100 or point["x"]==700:
                point["coord_mat"]=(point["coord_mat"][0]-3,point["coord_mat"][1])
            elif point["x"]==200 or point["x"]==600:
                point["coord_mat"]=(point["coord_mat"][0]-2,point["coord_mat"][1])
            else:
                point["coord_mat"]=(point["coord_mat"][0]-1,point["coord_mat"][1])
            plateau["état"][point["coord_mat"][0]][point["coord_mat"][1]]=nb
            for i in range(len(COORD_MAT)):
                if COORD_MAT[i]==point["coord_mat"]:
                    point["position"]=COORD[i]
            point["x"]=point["position"][0]
            point["y"]=point["position"][1]
            
        if j["direction"]=="bas":
            plateau["état"][point["coord_mat"][0]][point["coord_mat"][1]]=0
            if point["x"]==100 or point["x"]==700:
                point["coord_mat"]=(point["coord_mat"][0]+3,point["coord_mat"][1])
            elif point["x"]==200 or point["x"]==600:
                point["coord_mat"]=(point["coord_mat"][0]+2,point["coord_mat"][1])
            else:
                point["coord_mat"]=(point["coord_mat"][0]+1,point["coord_mat"][1])
            plateau["état"][point["coord_mat"][0]][point["coord_mat"][1]]=nb
            for i in range(len(COORD_MAT)):
                if COORD_MAT[i]==point["coord_mat"]:
                    point["position"]=COORD[i]
            point["x"]=point["position"][0]
            point["y"]=point["position"][1]
            
"""Fase 2 joueur"""
def changer_emplacement(souris_pos,selected,j,plateau):
    """
        (int,int), dico_pion , int, dico_plateau =>
        Déplace selected vers la position souris_pos
    """
    chercher_coord(selected,selected["position"][0],selected["position"][1])
    plateau["état"][selected["coord_mat"][0]][selected["coord_mat"][1]]=0
    selected["position"]=souris_pos
    valide_coord(selected)
    chercher_coord(selected,selected["x"],selected["y"])
    plateau["état"][selected["coord_mat"][0]][selected["coord_mat"][1]]=j

def direction_possible(pion,joueur,plateau):
    """
        dico_pion, dico_joueur, dico_plateau => Bool
        Teste si la direction est possible
    """
    x=pion["coord_mat"][0]
    y=pion["coord_mat"][1]
    if joueur["direction"]=="gauche":
        if y==0:
            return False
        else:
            for i in range(y-1,-1,-1):
                if plateau["état"][x][i]!=1 and plateau["état"][x][i]!=0:
                    return False
                if plateau["état"][x][i]==0:
                    return True
    if joueur["direction"]=="droite":
        if y==6:
            return False
        else:
            for i in range(y+1,7):
                if plateau["état"][x][i]!=1 and plateau["état"][x][i]!=0:
                    return False
                if plateau["état"][x][i]==0:
                    return True
    if joueur["direction"]=="haut":
        if x==0:
            return False
        else:
            for i in range(x-1,-1,-1):
                if plateau["état"][i][y]!=1 and plateau["état"][i][y]!=0:
                    return False
                if plateau["état"][i][y]==0:
                    return True
    if joueur["direction"]=="bas":
        if x==6:
            return False
        else:
            for i in range(x+1,7):
                if plateau["état"][i][y]!=1 and plateau["état"][i][y]!=0:
                    return False
                if plateau["état"][i][y]==0:
                    return True

def voisines(new_pion, pion,plateau):
    """
        dico_pion, dico_pion, dico_plateau => Bool
        Teste si new_pion est voisin de pion
    """
    if new_pion["x"]==pion["x"]:
        if pion["x"]==400 and pion["y"]<=180 and new_pion["x"]==400 and new_pion["y"]>180 :
            return False
        if pion["x"]==400 and pion["y"]>=320 and new_pion["x"]==400 and new_pion["y"]<320 :
            return False
        
        x=pion["coord_mat"][0]
        y=pion["coord_mat"][1]
        x2=new_pion["coord_mat"][0]
        y2=new_pion["coord_mat"][1]
        if x<len(plateau["état"])-1:
            i=x+1
            while i<(len(plateau["état"])-1) and plateau["état"][i][y]==1:
                i+=1
            if plateau["état"][i][y]==0 and (i==x2 and y==y2):
                return True
        if x>0:
            i=x-1
            while i>0 and plateau["état"][i][y]==1:
                i-=1
            if plateau["état"][i][y]==0 and (i==x2 and y==y2):
                return True
                
    if new_pion["y"]==pion["y"]:
        if pion["y"]==250 and pion["x"]<=300 and new_pion["y"]==250 and new_pion["x"]>=500 :
            return False
        if pion["y"]==250 and pion["x"]>=500 and new_pion["y"]==250 and new_pion["x"]<=300 :
            return False
        x=pion["coord_mat"][0]
        y=pion["coord_mat"][1]
        x2=new_pion["coord_mat"][0]
        y2=new_pion["coord_mat"][1]
        if y<len(plateau["état"][0])-1:
            j=y+1
            while j<(len(plateau["état"][0])-1) and plateau["état"][x][j]==1:
                j+=1
            if plateau["état"][x][j]==0 and (x==x2 and j==y2):
                return True
       
        if y>0:
            j=y-1
            while j>0 and plateau["état"][x][j]==1:
                j-=1
            if plateau["état"][x][j]==0 and (x==x2 and j==y2):
                return True
    return False
        

def chercher_direction_possible(pion,plateau):
    """
        dico_pion, dico_plateau => liste(str)
        Retourne la liste des directions possibles pour pion
    """
    x=pion["coord_mat"][0]
    y=pion["coord_mat"][1]
    direction=[]
    
    if x<len(plateau["état"])-1:
        if x!=2 or y!=3:
            i=x+1
            while i<(len(plateau["état"])-1) and plateau["état"][i][y]==1:
                i+=1
            if plateau["état"][i][y]==0 and (i!=2 or y!=3):
                direction.append("bas")
    
    if x>0:
        if x!=4 or y!=3:
            i=x-1
            while i>0 and plateau["état"][i][y]==1:
                i-=1
            if plateau["état"][i][y]==0 and (i!=4 or y!=3): 
                direction.append("haut")
    
    if y<len(plateau["état"][0])-1:
        if (x!=3 or y!=2):
            j=y+1
            while j<(len(plateau["état"][0])-1) and plateau["état"][x][j]==1:
                j+=1
            if plateau["état"][x][j]==0 and (x!=3 or j!=2):
                direction.append("droite")
       
    if y>0:
        if (x!=3 or y!=4):
            j=y-1
            while j>0 and plateau["état"][x][j]==1:
                j-=1
            if plateau["état"][x][j]==0 and (x!=3 or j!=4):
                direction.append("gauche")
    
    return direction

def deplace_pion(pion_o,plateau):
    """
        dico_pion, dico_plateau =>
        Deplace le pion de l'ordinateur dans une des directions possibles
    """
    emplacement_libre=[]
    for i in range(len(plateau["état"])):
        for j in range(len(plateau["état"][0])):
            if plateau["état"][i][j]==0:
                emplacement_libre.append((i,j))
    n=random.randint(0,len(emplacement_libre)-1)
    plateau["état"][pion_o["coord_mat"][0]][pion_o["coord_mat"][1]]=0
    pion_o["coord_mat"]=emplacement_libre[n]
    plateau["état"][emplacement_libre[n][0]][emplacement_libre[n][1]]=3
    for i in range(len(COORD_MAT)):
        if COORD_MAT[i]==pion_o["coord_mat"]:
            pion_o["position"]=COORD[i]
    pion_o["x"]=pion_o["position"][0]
    pion_o["y"]=pion_o["position"][1]
    
def deplace_pion_coord(pion_o,plateau,coord_mat):
    plateau["état"][pion_o["coord_mat"][0]][pion_o["coord_mat"][1]]=0
    pion_o["coord_mat"]=coord_mat
    plateau["état"][coord_mat[0]][coord_mat[1]]=3
    coord=chercher_coord_pygame(coord_mat[0],coord_mat[1])
    pion_o["position"]=coord
    pion_o["x"]=coord[0]
    pion_o["y"]=coord[1]
    
    
def pion_dessine(pion):
    """
        dico_pion => 
        Dessine le pion
    """
    pygame.draw.circle(pion["niv"],pion["couleur"],pion["position"],20)

