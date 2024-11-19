import pygame

def niveau_init(surface):
    """
        surface de dessin => rien
        Initialise le niveau
    """
    niveau={}
    niveau["surf"]=surface
    niveau["action"]="Placez vos pions sur le plateau"
    niveau["rect_joueur"]=(0,520,800,80)
    niveau["rect_jeu"]=(0,0,800,520)
    niveau["taille"]=30
    niveau["coord_text"]=(250,540)
    return niveau

def niveau_dessine(niveau):
    """
        dico des éléments de niveau => rien
        Dessine le niveau
    """
    pygame.draw.rect(niveau["surf"], (255,255,255), niveau["rect_joueur"])
    pygame.draw.rect(niveau["surf"], (0,0,0), niveau["rect_jeu"])
    
    """Moyen carrée"""
    pygame.draw.line(niveau["surf"],(255,255,255),(200,100),(600,100),10) #ligne du haut
    pygame.draw.line(niveau["surf"],(255,255,255),(200,100),(200,400),10) #ligne de gauche
    pygame.draw.line(niveau["surf"],(255,255,255),(200,400),(600,400),10) #ligne du bas
    pygame.draw.line(niveau["surf"],(255,255,255),(600,100),(600,400),10) 
    
    """Grand carrée"""
    pygame.draw.line(niveau["surf"],(255,255,255),(100,20),(700,20),10) #ligne du haut
    pygame.draw.line(niveau["surf"],(255,255,255),(100,20),(100,480),10) #ligne de gauche
    pygame.draw.line(niveau["surf"],(255,255,255),(100,480),(700,480),10) #ligne du bas
    pygame.draw.line(niveau["surf"],(255,255,255),(700,20),(700,480),10)
    
    """Petit carrée"""
    pygame.draw.line(niveau["surf"],(255,255,255),(300,180),(500,180),10) #ligne du haut
    pygame.draw.line(niveau["surf"],(255,255,255),(300,180),(300,320),10) #ligne de gauche
    pygame.draw.line(niveau["surf"],(255,255,255),(300,320),(500,320),10) #ligne du bas
    pygame.draw.line(niveau["surf"],(255,255,255),(500,180),(500,320),10)
    
    #Ligne qui relie les carrées
    pygame.draw.line(niveau["surf"],(255,255,255),(400,20),(400,180),10)
    pygame.draw.line(niveau["surf"],(255,255,255),(400,320),(400,480),10)
    
    pygame.draw.line(niveau["surf"],(255,255,255),(100,250),(300,250),10)
    pygame.draw.line(niveau["surf"],(255,255,255),(500,250),(700,250),10)
    
    #point grand carrée
    pygame.draw.rect(niveau["surf"], (155,97,196),(95,15,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(695,15,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(95,475,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(695,475,15,15))
    #point moyen carrée
    pygame.draw.rect(niveau["surf"], (155,97,196),(595,95,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(195,95,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(195,395,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(595,395,15,15))
    #point petit carrée
    pygame.draw.rect(niveau["surf"], (155,97,196),(295,175,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(495,175,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(295,315,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(495,315,15,15))
    
    pygame.draw.rect(niveau["surf"], (155,97,196),(395,15,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(395,175,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(395,315,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(395,475,15,15))
    
    pygame.draw.rect(niveau["surf"], (155,97,196),(95,245,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(295,245,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(495,245,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(695,245,15,15))
    
    pygame.draw.rect(niveau["surf"], (155,97,196),(395,95,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(395,395,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(195,245,15,15))
    pygame.draw.rect(niveau["surf"], (155,97,196),(595,245,15,15))
    
    mettre_a_jour_affichage(niveau,niveau["action"],niveau["coord_text"],niveau["taille"])
    
def mettre_a_jour_affichage(niveau,text,coord,taille):
    """
        dico_niveau, str, (int,int), int =>
        Met à jour l'affichage avec le text de taille taille et aux coordonnées coord
    """
    pygame.draw.rect(niveau["surf"], (255,255,255), niveau["rect_joueur"])
    changer_action(niveau,text,coord,taille)
    image_joueur=pygame.font.SysFont("Times New Roman",niveau["taille"]).render(text,1,(200,55,255))
    niveau["surf"].blit(image_joueur,niveau["coord_text"])
    
def changer_action(niveau,text,coord,taille):
    """
        dico_niveau, str, (int,int), int =>
        Modifie le dico_niveau pour changer l'affichage de l'action en cours
    """
    niveau["action"]=text
    niveau["coord_text"]=coord
    niveau["taille"]=taille
    