import pygame
from niveau import *
from pion import *
from jeu import *
from joueur import *

def main():
    """Fonction principale du programme"""

    pygame.init()
    horloge = pygame.time.Clock()
    surface = pygame.display.set_mode((800,600))
    img=pygame.image.load('moulin.png')
    pygame.display.set_icon(img)
    pygame.display.set_caption("Jeu du moulin")
    continuer = True
    j=init_joueur()
    plateau=init_plateau(2)
    niveau=niveau_init(surface)
    ouverture(surface)
    pygame.time.wait(5000)
    o=init_ordi()
    passer=True
    #booleen qui permet de savoir si un pion a bien été enlevée apres la formation d'un moulin
    pion_pas_enlever=False
    #booleen qui permet de savoir si un pion a été selectionner pour le déplacer
    selected=None
    
    while continuer:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                continuer = False
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    j["direction"]="gauche"
                elif event.key==pygame.K_RIGHT:
                    j["direction"]="droite"
                elif event.key==pygame.K_UP:
                    j["direction"]="haut"
                elif event.key==pygame.K_DOWN:
                    j["direction"]="bas"
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                #récupérer les coordonnées de la souris
                souris_pos=event.pos
                
                #1er fase
                #Poser 9 pions sur le plateau
                if plateau["fase"]==0  and j["pion_place"]<=9:
                    mettre_a_jour_affichage(niveau,"Placez vos pions sur le plateau",(250,540),30)
                    if plateau["joueur_courant"]==2:
                        pion=pion_init(surface,souris_pos,(192,192,192))
                        if valide_coord(pion):
                            chercher_coord(pion,pion["x"],pion["y"])
                            if plateau["état"][pion["coord_mat"][0]][pion["coord_mat"][1]]==0:
                                mettre_a_jour_matrice(plateau,pion["coord_mat"],2)
                                ajoute_pion_liste(j,pion)
                                changer_joueur_courant(plateau,3)
                                
                    
                    if test_moulin(j["liste_pion"],j) or pion_pas_enlever :
                        mettre_a_jour_affichage(niveau,"Vous avez formé un moulin, choisissez un pion adverse",(85,540),30)
                        pion_enleve=trouver_pion_correspondant(o["liste_pion"],souris_pos)
                        pion_pas_enlever=True
                        if pion_enleve != None:
                            chercher_coord(pion_enleve,pion_enleve["position"][0],pion_enleve["position"][1])
                            retirer_pion(o,pion_enleve,plateau)
                            pion_pas_enlever=False
                            
                #2e fase
                #On sélectionne un pion puis on le bouge vers une case voisine
                if plateau["fase"]==1:
                    mettre_a_jour_affichage(niveau,"Déplacer un pion en cliquant sur le pion à déplacer puis sur l'endroit où le déplacer",(25,550),22)
                    if plateau["joueur_courant"]==2:
                        #teste si on a bien selectionné un pion connu
                        pion=trouver_pion_correspondant(j["liste_pion"],souris_pos)
                        if (pion != None or selected != None) and selected != pion:
                            if selected:
                                new_position=pion_init(surface,souris_pos,(192,192,192))
                                #verifie que le nouvel emplacement du pion est valide
                                if valide_coord(new_position):
                                    #regarde si l'utilisateur n'a pas changé d'avis
                                    #c'est à dire vérifie que la nouvelle position n'est pas en réalité un autre pion de j
                                    if est_dans_liste_pion(j["liste_pion"],new_position):
                                        #si c'est le cas il deviens le nouveau pion sélectionner
                                        selected=trouver_pion(j["liste_pion"],new_position)
                                    else:
                                        chercher_coord(new_position,new_position["x"],new_position["y"])
                                        #on vérifie donc que new_position et le pion sélectionné sont voisines sinon le déplacement n'est pas possible
                                        if voisines(new_position,selected,plateau):
                                            changer_emplacement(souris_pos,selected,2,plateau)
                                            selected=None
                                            changer_joueur_courant(plateau,3)
                            else:
                                #stocke le pion choisi
                                selected=pion


                        if test_moulin(j["liste_pion"],j) or pion_pas_enlever:
                            mettre_a_jour_affichage(niveau,"Vous avez formé un moulin, choisissez un pion adverse",(85,540),30)
                            pion_enleve=trouver_pion_correspondant(o["liste_pion"],souris_pos)
                            pion_pas_enlever=True
                            if pion_enleve != None:
                                chercher_coord(pion_enleve,pion_enleve["position"][0],pion_enleve["position"][1])
                                retirer_pion(o,pion_enleve,plateau)
                                pion_pas_enlever=False
                          
                #3e fase
                #On peut bouger où on veut si le nb de pion de joueur atteint 3 sinon même déplacement que pour la fase 1
                if plateau["fase"]==2:
                    #le cas où le nombre de pion de j est égal à 3
                    #on peut donc se déplacer où on veut sur les cases du plateau non occupées
                    if j["nb_pion"]==3 and plateau["joueur_courant"]==2:
                        mettre_a_jour_affichage(niveau,"Déplacez vos pions où vous voulez",(250,540),30)
                        pion=trouver_pion_correspondant(j["liste_pion"],souris_pos)
                        if (pion != None or selected != None) and selected != pion:
                            if selected:
                                new_position=pion_init(surface,souris_pos,(192,192,192))
                                if est_dans_liste_pion(j["liste_pion"],new_position):
                                    selected=trouver_pion(j["liste_pion"],new_position)
                                else:
                                    if verifier_coord(souris_pos,o["liste_pion"],j["liste_pion"]):
                                        changer_emplacement(souris_pos,selected,2,plateau)
                                        selected=None
                                        changer_joueur_courant(plateau,3)
                            else:
                                selected=pion
                    
                    #le cas où le nombre de pion de j est supérieur à 3
                    #on peut donc déplacer les pions que dans leurs cases voisines
                    elif plateau["joueur_courant"]==2:
                        mettre_a_jour_affichage(niveau,"Déplacer un pion en cliquant sur le pion à déplacer puis sur l'endroit où le déplacer",(25,550),22)
                        pion=trouver_pion_correspondant(j["liste_pion"],souris_pos)
                        if (pion != None or selected != None) and selected != pion:
                            if selected:
                                new_position=pion_init(surface,souris_pos,(192,192,192))
                                if valide_coord(new_position):
                                    if est_dans_liste_pion(j["liste_pion"],new_position):
                                        selected=trouver_pion(j["liste_pion"],new_position)
                                    else:
                                        chercher_coord(new_position,new_position["x"],new_position["y"])
                                        if voisines(new_position,selected,plateau):
                                            changer_emplacement(souris_pos,selected,2,plateau)
                                            selected=None
                                            changer_joueur_courant(plateau,3)
                            else:
                                selected=pion
                                
                    if test_moulin(j["liste_pion"],j) or pion_pas_enlever:
                        mettre_a_jour_affichage(niveau,"Vous avez formé un moulin, choisissez un pion adverse",(85,540),30)
                        pion_enleve=trouver_pion_correspondant(o["liste_pion"],souris_pos)
                        pion_pas_enlever=True
                        if pion_enleve != None:
                            chercher_coord(pion_enleve,pion_enleve["position"][0],pion_enleve["position"][1])
                            retirer_pion(o,pion_enleve,plateau)
                            pion_pas_enlever=False          
                                    

                    
                            
        #Ordi
        if plateau["joueur_courant"]==3 and plateau["fase"]==0:
            #regarde si 2 pions de la liste moulin sont alignés 
            liste_des_possibilites_moulin=test_2_pions_alignes(o["liste_pion"])
            if liste_des_possibilites_moulin != []:
                #recherche la coordonnées manquante pour former un moulin et regarde si c'est possible d'y mettre un pion
                coord_mat,i=chercher_coord_manquant(liste_des_possibilites_moulin,j["liste_pion"],plateau)
                if coord_mat != None:
                    #met le pion à la coordonnée manquante disponible pour former un moulin
                    mettre_a_jour_matrice(plateau,coord_mat,3)
                    coord=chercher_coord_pygame(coord_mat[0],coord_mat[1])
                    pion_o=pion_init(niveau["surf"],coord,(119,181,254))
                    
                #si 3e coordonnées non disponibles
                else:
                    #bloquer le joueur pour pas qu'il forme un moulin
                    liste_des_possibilites_moulin_j=test_2_pions_alignes(j["liste_pion"])
                    if liste_des_possibilites_moulin_j != []:
                        #chercher la coordonnée manquante au moulin du joueur si coordonnée libre on met un pion
                        coord_mat,i=chercher_coord_manquant(liste_des_possibilites_moulin_j,o["liste_pion"],plateau)
                        if coord_mat != None:
                            mettre_a_jour_matrice(plateau,coord_mat,3)
                            coord=chercher_coord_pygame(coord_mat[0],coord_mat[1])
                            pion_o=pion_init(niveau["surf"],coord,(119,181,254))
                        else:
                            #ajoute un pion dans un des angles du plus grand carrée
                            liste=angle_carre_grand_libre(plateau)
                            if liste != []:
                                pion_o=placer_pion_angle_libre(liste,niveau,plateau)
                            else:
                                #ajoute un pion dans un des angles du moyen carrée
                                liste=angle_carre_moyen_libre(plateau)
                                if liste != []:
                                    pion_o=placer_pion_angle_libre(liste,niveau,plateau)
                                else:
                                    #si aucun cas possible on choisi une position aléatoire
                                    pion_o=choisir_emplacement_ordi(o,j,niveau,plateau)
                        
                    else:
                        #ajoute un pion dans un des angles du plus grand carrée
                        liste=angle_carre_grand_libre(plateau)
                        if liste != []:
                            pion_o=placer_pion_angle_libre(liste,niveau,plateau)
                        else:
                            #ajoute un pion dans un des angles du moyen carrée
                            liste=angle_carre_moyen_libre(plateau)
                            if liste != []:
                                pion_o=placer_pion_angle_libre(liste,niveau,plateau)
                            else:
                                pion_o=choisir_emplacement_ordi(o,j,niveau,plateau)
            
            #Si aucun des pions de l'ordinateur n'est aligné
            else:
                #on regarde si le joueur peut potentiellement former un moulin
                liste_des_possibilites_moulin_j=test_2_pions_alignes(j["liste_pion"])
                if liste_des_possibilites_moulin_j != []:
                    coord_mat,i=chercher_coord_manquant(liste_des_possibilites_moulin_j,o["liste_pion"],plateau)
                    if coord_mat != None:
                        mettre_a_jour_matrice(plateau,coord_mat,3)
                        coord=chercher_coord_pygame(coord_mat[0],coord_mat[1])
                        pion_o=pion_init(niveau["surf"],coord,(119,181,254))
                    else:
                        #ajoute un pion dans un des angles du plus grand carrée
                        liste=angle_carre_grand_libre(plateau)
                        if liste != []:
                            pion_o=placer_pion_angle_libre(liste,niveau,plateau)
                        else:
                            #ajoute un pion dans un des angles du moyen carrée
                            liste=angle_carre_moyen_libre(plateau)
                            if liste != []:
                                pion_o=placer_pion_angle_libre(liste,niveau,plateau)
                            else:
                                pion_o=choisir_emplacement_ordi(o,j,niveau,plateau)
                
                else:
                    liste=angle_carre_grand_libre(plateau)
                    if liste != []:
                        #placer un pion a un grand angle libre
                        pion_o=placer_pion_angle_libre(liste,niveau,plateau)
                    else:
                        #placer un pion a un moyen angle libre
                        liste=angle_carre_moyen_libre(plateau)
                        if liste != []:
                            pion_o=placer_pion_angle_libre(liste,niveau,plateau)
                        else:
                            pion_o=choisir_emplacement_ordi(o,j,niveau,plateau)
            
            chercher_coord(pion_o,pion_o["position"][0],pion_o["position"][1])
            ajoute_pion_liste(o,pion_o)
            pion_o["x"]=pion_o["position"][0]
            pion_o["y"]=pion_o["position"][1]
            changer_joueur_courant(plateau,2)
                    
        #2e fase ou 3e fase si l'ordinateur a plus de 3 pions
        #déplacement dans des cases voisines
        if (plateau["joueur_courant"]==3 and plateau["fase"]==1) or (plateau["joueur_courant"]==3 and plateau["fase"]==2 and o["nb_pion"]>3):
            #teste si le joueur a 2 pions alignés
            liste_des_possibilites_moulin_j=test_2_pions_alignes(j["liste_pion"])
            #regarde quel est le meilleur pion a bouger en fonction de la situation
            nouveau_pion=trouver_meilleur_pion_bouger(o["liste_pion"],plateau,o,liste_des_possibilites_moulin_j)
            #si on ne trouve pas de meilleur pion, on va chercher un pion a bouger qui ne bloque pas l'ennemi
            if nouveau_pion == None:
                pion_o=choisir_pion(o["liste_pion"])
                liste_direction=chercher_direction_possible(pion_o,plateau)
                if not(permet_de_former_un_moulin(liste_des_possibilites_moulin_j,pion_o)):
                    if liste_direction != []:
                        choisir_direction(o,liste_direction)
                        changer_coord(pion_o,pion_o["position"][0],pion_o["position"][1],o,plateau,3)
                        changer_joueur_courant(plateau,2)
            else:
                changer_joueur_courant(plateau,2)
    
        #3e fase
        #On peut bouger le pion où on veut si nb pion de ordi est égal à 3
        if plateau["fase"]==2 and o["nb_pion"]==3 and plateau["joueur_courant"]==3 :
            #Les possibiltés pour l'ordinateur de formé un moulin
            liste_des_possibilites_moulin_o=test_2_pions_alignes(o["liste_pion"])
            if liste_des_possibilites_moulin_o != []:
                coord_mat,i=chercher_coord_manquant(liste_des_possibilites_moulin_o,j["liste_pion"],plateau)
                if coord_mat != None:
                    pion_o=chercher_3e_pion(o["liste_pion"],liste_des_possibilites_moulin_o[i])
                    deplace_pion_coord(pion_o,plateau,coord_mat)
                    changer_joueur_courant(plateau,2)
                else:
                    pion_o=choisir_pion(o["liste_pion"])
                    deplace_pion(pion_o,plateau)
                    changer_joueur_courant(plateau,2)
            
            else:
                #Les possibilités que le joueur forme un moulin
                liste_des_possibilites_moulin_j=test_2_pions_alignes(j["liste_pion"])
                if liste_des_possibilites_moulin_j != []:
                    coord_mat,i=chercher_coord_manquant(liste_des_possibilites_moulin_j,o["liste_pion"],plateau)
                    if coord_mat != None:
                        pion_o=choisir_pion(o["liste_pion"])
                        deplace_pion_coord(pion_o,plateau,coord_mat)
                        changer_joueur_courant(plateau,2)
                    else:
                        #choisir aléatoirement
                        pion_o=choisir_pion(o["liste_pion"])
                        deplace_pion(pion_o,plateau)
                        changer_joueur_courant(plateau,2)
                else:
                    #choisir aléatoirement
                    pion_o=choisir_pion(o["liste_pion"])
                    deplace_pion(pion_o,plateau)
                    changer_joueur_courant(plateau,2)
                    
        #test moulin pour l'ordinateur
        if not(pion_pas_enlever) and test_moulin(o["liste_pion"],o):
            mettre_a_jour_affichage(niveau,"L'ordinateur a formé un moulin",(250,540),30)
            if plateau["fase"]==0:
                #enleve un pion en dehors d'un moulin
                pion_enleve_o=choisir_pion_non_moulin(j["moulin"],j["liste_pion"])
                retirer_pion(j,pion_enleve_o,plateau)
            else:
                if j["moulin"] != []:
                    #enleve un pion d'un moulin
                    pion_enleve_o=choisir_pion_moulin(j["moulin"],j["liste_pion"])
                    retirer_pion(j,pion_enleve_o,plateau)
                else:
                    #choisi aléatoirement un pion sinon
                    pion_enleve_o=choisir_pion(j["liste_pion"])
                    retirer_pion(j,pion_enleve_o,plateau)
        
        #vérifie si un pion qui former un moulin n'a pas été bouger et donc le moulin n'existe plus
        pion_moulin_bouger(j["liste_pion"], j["moulin"])
        pion_moulin_bouger(o["liste_pion"], o["moulin"])
                        
        if bloquer(j["liste_pion"],plateau):
            print("à cause de bloquer ")
            affiche_plateau(plateau["état"])
            fermeture(2,surface,niveau)
            pygame.time.wait(5000)
            continuer=False
            
        if bloquer(o["liste_pion"],plateau):
            print("à cause de bloquer ordi")
            affiche_plateau(plateau["état"])
            fermeture(3,surface,niveau)
            pygame.time.wait(5000)
            continuer=False
        
        if plateau["fase"]==2:
            #le joueur a perdu
            if j["nb_pion"]==2:
                fermeture(2,surface,niveau)
                pygame.time.wait(5000)
                continuer=False
            #l'ordi a perdu
            if o["nb_pion"]==2:
                fermeture(3,surface,niveau)
                pygame.time.wait(5000)
                continuer=False
                        
        if j["pion_place"]==9 and passer:
            passer=False
            changer_fase(plateau)
            
        if plateau["fase"]==1 and (j["nb_pion"]==3 or o["nb_pion"]==3):
            plateau["fase"]=2
        
        niveau_dessine(niveau)
        dessiner_pions_joueurs(j["liste_pion"])
        dessiner_pions_joueurs(o["liste_pion"])
        pygame.display.update()
        horloge.tick(15)
    pygame.quit()

def ouverture(surface):
    """
        surface de dessin => rien
        Dessine la page d'ouverture
    """
    police=pygame.font.SysFont("Times New Roman",65)
    image_texte=police.render("Le jeu du moulin",1,(255,255,255))
    surface.blit(image_texte,(200,30))
    
    police2=pygame.font.SysFont("Times New Roman",25)
    image_texte2=police2.render("by Manon Davion",1,(255,255,255))
    surface.blit(image_texte2,(500,90))
    
    image_instruction=police2.render("Fase 1: ",1,(255,255,255))
    surface.blit(image_instruction,(100,150))
    image_instruction2=police2.render("Cliquer avec la souris pour mettre les pions",1,(255,255,255))
    surface.blit(image_instruction2,(130,200))
    
    image_instruction3=police2.render("Fase 2: ",1,(255,255,255))
    surface.blit(image_instruction3,(100,250))
    image_instruction4=police2.render("Cliquer sur le pion puis sur une des cases pour le déplacer",1,(255,255,255))
    surface.blit(image_instruction4,(130,300))
    
    image_instruction5=police2.render("Fase 3: ",1,(255,255,255))
    surface.blit(image_instruction5,(100,350))
    image_instruction6=police2.render("Cliquer sur le pion et déplacer le où vous voulez ",1,(255,255,255))
    surface.blit(image_instruction6,(130,400))
    
    image_instruction7=police2.render("Vous jouez contre l'ordinateur",1,(255,255,255))
    surface.blit(image_instruction7,(100,450))
    
    image_version=police2.render("Version 2.1 ",1,(255,255,255))
    surface.blit(image_version,(680,530))
    
    image_date=police2.render("07/12/2023",1,(255,255,255))
    surface.blit(image_date,(680,560))
    pygame.display.flip()
    
def fermeture(j,surface,niveau):
    if j==2:
        pygame.draw.rect(niveau["surf"], (0,0,0), (0,0,800,600))
        police=pygame.font.SysFont("Times New Roman",30)
        image_texte=police.render("Vous avez perdu",1,(255,255,255))
        surface.blit(image_texte,(230,270))
    if j==3:
        pygame.draw.rect(niveau["surf"], (0,0,0), (0,0,800,600))
        police=pygame.font.SysFont("Times New Roman",40)
        image_texte=police.render("Vous avez battu l'ordinateur",1,(255,255,255))
        surface.blit(image_texte,(200,270))
    pygame.display.flip()

if __name__ == "__main__":
    main()