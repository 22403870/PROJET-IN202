
#projet UVSQolor le but du projet consiste a cree un logiciel dans lequel on peut manipuler des images ce programme devra : 

# permettre d'ouvrir une image 
# proposer plusieurs filtre et algorithme de modification 
# permettre de sauvegarder une image 
#gerer un historique d'action


#une image avec plusieurs filtres les filtres que nous devrons coder seront :


#filtre vert rouge bleu rgb 
#Filtre gris 
#Luminositer (correction gamma)
#contraste  (correction sigma)
#flou uniforme
#flou gaussien
#filtre de detection de bord 
#fusion d'image

#autre choix (zoom d'image par ex,redimensionner l'image par exemple, rotate ect )




# nous crerons l'interface graphique avec tkinter le but sera de cree un canva dans lequel l'utilisateur qui lance le code pourra modifier n'importe quel image 
#cela suppose que nous devons pas importer notre image mais nous devons avoir acces a la bibliotheque personel de l'utilisateur comme on a fait 
#pour le projet 2048 pour charger le fichier que nous avons enregistrer (voir la syntaxe dans le projet 2048) on crera une fonction #charger l'image pour cette etape 

# ne supprimer pas les instructions en # elles nous seront utile pour la suite et aussi pour avoir un apercu de ce que nous devons faire 






#DEBUT DU CODE DU PROJET 




# Bibliotheque utile 

import numpy as np
import tkinter as tk
from tkinter import filedialog 
from PIL import Image
from PIL import Image, ImageTk, ImageFilter
import pathlib
from scipy.signal import convolve2d
import math 






#interface

racine = tk.Tk()
racine.title('UVSQolor')

canvas = tk.Canvas(racine, width=950, height=800, bg="#5d5c5e")
canvas.grid(row=0, column=0)





# ON CREE LES MENUS A L'AVANCE POUR LES APPELER DANS NOS FONCTIONS PLUS TARD 

menu_principal = tk.Menu(racine)                                 
menu_fichier = tk.Menu(menu_principal, tearoff=0)


menu_principal.add_cascade(label="Fichier",  menu=menu_fichier)           
racine.config(menu=menu_principal)








# ESPACE MODIFIER OU IL VA Y AVOIR LES DIFFERENTS FILTRES 
# C'EST ICI QU'ON CREE TOUT LES CALLBACKS DANS LE MENU PRINCIPAL 

menu_edit = tk.Menu(menu_principal, tearoff=0)                              # autre menu modifier on pourra mettre les filtres dedans 
menu_principal.add_cascade(label="Modifier", menu=menu_edit) 

menu_filtre = tk.Menu(menu_principal, tearoff=0)                              # autre menu modifier on pourra mettre les filtres dedans 
menu_principal.add_cascade(label="Filtre", menu=menu_filtre) 








#FONCTION POUR OUVRIR ENREGISTRER ET QUITTER 


def open_fichier():
    global image_loader, image

    # Ouvre une boîte de dialogue pour choisir une image
    fichier_path = filedialog.askopenfilename(
        defaultextension=".png",
        filetypes=[("Images", "*.png *.jpeg *.jpg")])

    if fichier_path:
        image_loader = Image.open(fichier_path).convert('RGB')
        image_loader = image_loader.resize((475, 300))
        image_canva(canvas, racine)
    return fichier_path

menu_fichier.add_command(label="Open", command=open_fichier)



def save_image():                                      
    global image, uvsq_root , canvas_used

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Images", "*.png *.jpeg *.jpg")])
    if file_path:
        with open(file_path, 'w') as file:                              #enregistre le fichier dans la bibliotheque de l'utilisateur 
            file.write(image)
menu_fichier.add_command(label="Enregistrer", command=save_image) # cascade dans le callback du menu principal fichier  



def quitter_racine():                  
    racine.destroy()
menu_fichier.add_command(label="Quitter", command=quitter_racine) # sous callback du menu principal fichier 




# ESPACE OU L'ON PEUT METTRE LES BOUTONS                                                 
frame_controle = tk.Frame(racine)
frame_controle.grid(row=0, column=1) 



def bouton_arriere():  # fonction bouton arriere 
    global image 
    
# A COMPLETER POUR L'HISTORIQUE DES TOUTCHES 
arriere = tk.Button(frame_controle, text="←", font=("Helvetica", 20, "bold"), bg="#5a9e81", fg="white", relief="flat", command=bouton_arriere)  # vérifie a chaque fin de déplacement si on a pas une fin possible
arriere.grid(row=1, column=0, padx=5)


 
def bouton_avant():  # fonction bouton avant 
    global image 
 # A COMPLETER POUR L'HISTORIQUE DES MODIFICATIONS 
avant = tk.Button(frame_controle, text="→", font=("Helvetica", 20, "bold"), bg="#5a9e81", fg="white", relief="flat", command=bouton_avant)  # vérifie a chaque fin de déplacement si on a pas une fin possible
avant.grid(row=1, column=2, padx=5)


# FIN DE L'INTERFACE  


# CHARGER UNE 2E IMAGE ON VERRA SA PLUS TARD

def charger_deuxieme_image():
    global image_loader_2
    path_image_2 = filedialog.askopenfilename(title="Choisir la deuxième image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    
    if path_image_2:
        image_loader_2 = Image.open(path_image_2)  # Charger la deuxième image
    else:
        print("Aucune image sélectionnée.")

menu_fichier.add_command(label="Charger deuxième image", command=charger_deuxieme_image)








# ON DOIT DEFINIR LES PIXELS RGB        # ON DOIT REVOIR CAR C'EST TROP CHATGPT JE CROIS 
def rgb_pixel(pixel):
	r,g,b = pixel
	return (r+g+b)//3


def average_pix(pixel):
	r,g,b = pixel
	return (r+g+b)//3


# FONCTION 
def get_pixel_rgb(x, y,image = ''):
	if image == '':
		image=image_loader
	return image.getpixel((x, y))

def image_path(image_name):
	return f'{pathlib.Path(__file__).parent.resolve()}/{image_name}'

global image_history_filters , image_history_redo, image_save
image_history_filters = []
image_history_redo = [] #si on veut remettre la photo comme elle etait avant le Redo
canvas_created = False
image_save = ''

def add_history(image):
	image_history_filters.append(np.array(image))
      
def image_canva(background_canva , uvsq_root):
	global image
	image = ImageTk.PhotoImage(image_loader)
	def canvas_create_funct(uvsq_root):
		print('working')
		global canvas_created, image_canvas , canvas_used
		canvas_used = background_canva
		canvas_created = True
		image_canvas = background_canva.create_image(0, 0,
							image = image,
				         anchor = "nw")
	if canvas_created:
		background_canva.itemconfig(image_canvas  , image=image)
	else:
		canvas_create_funct(uvsq_root)






# FONCTIONNALITER DES EFFECT POUR APPLIQUER ET ANNULER  

def applique_effet(background_canva , uvsq_root, image_name = 'modified_image.jpg' , image_redo = False):
	global image , image_loader , image_history_redo
	image_loader = Image.open(image_path(image_name))
	add_history(np.array(image_loader.convert("RGB")))
	if not image_redo:
		image_history_redo = []
	image_canva(background_canva , uvsq_root)
    

      
def annule_effect(root):     
	global image , image_loader
	image_loader = Image.open(open_fichier)
	image_canva(canvas_used , root)










#FILTRE RGB 

def red_filter():    # FILTRE ROUGE (ANITA)
    global image, image_loader

    pixels = np.array(image_loader.convert('RGB'))

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            r, _, _ = pixels[y, x]
            pixels[y, x] = (r, 0, 0)

    image_loader = Image.fromarray(pixels)
    add_history(image_loader)
    image_canva(canvas, racine)

menu_filtre.add_command(label="filtre rouge", command=red_filter)



def blue_filter():                        #(BAYEK)
    global image, image_loader

    # On part de image_loader, qui est bien une image PIL
    pixels = np.array(image_loader.convert('RGB'))

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            _, _, b = pixels[y, x]
            pixels[y, x] = (0, 0, b)

    # On crée une nouvelle image depuis les pixels
    image_loader = Image.fromarray(pixels)

    # On met à jour l’historique si tu veux gérer undo/redo
    add_history(image_loader)

    # On affiche l’image modifiée dans le canvas
    image_canva(canvas, racine)
menu_filtre.add_command(label="filtre bleu", command=blue_filter)


def filtre_vert():                           #(YANN)
    global image, image_loader

    pixels = np.array(image_loader.convert('RGB'))

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            r, g, b = pixels[y, x]
            pixels[y, x] = (0, g, 0)

    image_loader = Image.fromarray(pixels)


    add_history(image_loader)

    image_canva(canvas, racine)

menu_filtre.add_command(label="filtre vert", command=filtre_vert)




# FILTRE GRIS

def gray_filter():    #(ANITA)
    global image, image_loader

    pixels = np.array(image_loader.convert('RGB'))

    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            r, g, b = pixels[y, x]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            pixels[y, x] = (gray, gray, gray)

    image_loader = Image.fromarray(pixels)
    add_history(image_loader)
    image_canva(canvas, racine)

menu_filtre.add_command(label="filtre gris", command=gray_filter)













#FILTRE LUMINOSITER

def luminosite():                        #(BAYEK)
    global interface_luminosite
    interface_luminosite = tk.Toplevel(racine)
    interface_luminosite.title("Luminosité")
    interface_luminosite.geometry("300x180")
    interface_luminosite.grab_set()

    # Slider de luminosité
    tk.Label(interface_luminosite, text="Luminosité (0.5 - 10.0) :").pack()
    slider = tk.Scale(interface_luminosite, from_=0.5, to=10.0,
                      orient=tk.HORIZONTAL, length=200,
                      resolution=0.1, digits=3)
    slider.set(1.0)
    slider.pack(pady=10)

    # Frame pour les boutons
    bouton_frame = tk.Frame(interface_luminosite)
    bouton_frame.pack(side=tk.BOTTOM, pady=10)

    # Appliquer la luminosité directement sans fonction séparée
    def ajuster_luminosite():
        global image_loader
        facteur = slider.get()

        # Appliquer la luminosité pixel par pixel
        pixels = np.array(image_loader.convert('RGB'))
        for y in range(pixels.shape[0]):
            for x in range(pixels.shape[1]):
                r, g, b = pixels[y, x]
                r = min(int(r * facteur), 255)
                g = min(int(g * facteur), 255)
                b = min(int(b * facteur), 255)
                pixels[y, x] = (r, g, b)

        image_loader_mod = Image.fromarray(pixels.astype(np.uint8))
        image_loader = image_loader_mod
        add_history(image_loader)
        image_canva(canvas, racine)
        interface_luminosite.destroy()

    # Boutons
    bouton_appliquer = tk.Button(bouton_frame, text="Appliquer",  font=("Arial", 10), bg="#f7dcdc", command=ajuster_luminosite)
    bouton_appliquer.pack(side=tk.LEFT, padx=10)
    bouton_annuler = tk.Button(bouton_frame, text="Annuler",  font=("Arial", 10), bg="#f7dcdc", command=interface_luminosite.destroy)
    bouton_annuler.pack(side=tk.RIGHT, padx=10)

# Ajout au menu
menu_edit.add_command(label="Luminosité", command=luminosite)








# FILTRE CONTRASTE


def contraste():     #(ANITA)
    global interface_contraste
    interface_contraste = tk.Toplevel(racine)
    interface_contraste.title("Contraste")
    interface_contraste.geometry("300x200")
    interface_contraste.grab_set()

    # Slider facteur de contraste
    intensité = tk.Label(interface_contraste, text="contrast 0.5 - 10.0 :")
    intensité.pack()
    slider_facteur = tk.Scale(interface_contraste, from_=0.5, to=10.0,
                              orient=tk.HORIZONTAL, length=200,
                              resolution=0.1, digits=3)
    slider_facteur.set(5.0)
    slider_facteur.pack(pady=10)

    # Boutons
    bouton = tk.Frame(interface_contraste)
    bouton.pack(side=tk.BOTTOM, pady=10)

    def appliquer_contraste():
        global image_loader
        facteur = slider_facteur.get()

        def sigmoide(val):
            val_norm = val / 255.0
            contrasté = 1 / (1 + math.exp(-facteur * (val_norm - 0.5)))  # 0.5 = milieu
            return int(contrasté * 255)

        pixels = np.array(image_loader.convert('RGB'))

        for y in range(pixels.shape[0]):
            for x in range(pixels.shape[1]):
                r, g, b = pixels[y, x]
                pixels[y, x] = (sigmoide(r), sigmoide(g), sigmoide(b))

        image_loader_mod = Image.fromarray(pixels.astype(np.uint8))
        image_loader = image_loader_mod
        add_history(image_loader)
        image_canva(canvas, racine)
        interface_contraste.destroy()

    bouton_appliquer = tk.Button(bouton, text="Appliquer", font=("Arial", 10), bg="#f7dcdc", command=appliquer_contraste)
    bouton_appliquer.pack(side=tk.LEFT, padx=10)

    bouton_annuler = tk.Button(bouton, text="Annuler", font=("Arial", 10), bg="#f7dcdc", command=interface_contraste.destroy)
    bouton_annuler.pack(side=tk.LEFT, padx=10)

menu_edit.add_command(label="contraste", command=contraste)




# FILTRE FLOU 

def filtre_de_flou(img, rayon):   #(BAYEK)
    if rayon == 0:
        return img
    arr = np.array(img.convert("RGB"))
    h, w, c = arr.shape
    k = 2 * rayon + 1
    arr_padded = np.pad(arr, ((rayon, rayon), (rayon, rayon), (0, 0)), mode='edge')
    cumsum = arr_padded.cumsum(axis=0).cumsum(axis=1)
    A = cumsum[k:, k:]
    B = cumsum[:-k, k:]
    C = cumsum[k:, :-k]
    D = cumsum[:-k, :-k]
    somme = A - B - C + D
    moyenne = somme // (k * k)
    moyenne = np.clip(moyenne, 0, 255).astype(np.uint8)
    return Image.fromarray(moyenne)


def flou():
    fenetre = tk.Toplevel(racine)
    fenetre.title("Flou")
    fenetre.geometry("300x150")
    fenetre.grab_set()

    tk.Label(fenetre, text="Rayon du flou (0 à 10) :").pack()
    slider = tk.Scale(fenetre, from_=0, to=10, orient=tk.HORIZONTAL)
    slider.set(0)
    slider.pack(pady=10)

    def appliquer():
        global image_loader
        rayon = slider.get()
        if image_loader is not None:
            image_loader_mod = filtre_de_flou(image_loader, rayon)
            image_loader = image_loader_mod
            add_history(image_loader)
            image_canva(canvas, racine)
            fenetre.destroy()

    tk.Button(fenetre, text="Appliquer", font=("Arial", 10), bg="#f7dcdc", command=appliquer).pack(side=tk.LEFT, padx=20, pady=10)
    tk.Button(fenetre, text="Annuler", font=("Arial", 10), bg="#f7dcdc", command=fenetre.destroy).pack(side=tk.RIGHT, padx=20, pady=10)

menu_edit.add_command(label="Flou uniforme", command=flou)







# Fonction pour créer le noyau du filtre gaussien
def noyau_filtre_gauss(taille, sigma):  # (YANN)
    noyau = np.zeros((taille, taille))
    pixel_principale = taille // 2

    for i in range(taille):
        for j in range(taille):
            x = i - pixel_principale
            y = j - pixel_principale
            noyau[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    noyau /= np.sum(noyau)  # Normalisation du noyau

    return noyau

# Fonction pour appliquer le flou gaussien
def flou_gaussien(taille, sigma):
    global image_loader  # image_loader est la variable contenant l'image originale

    # Conversion de l'image en tableau numpy
    pixels = np.array(image_loader.convert('RGB'))

    # Création du noyau de filtre gaussien
    noyau_final = noyau_filtre_gauss(taille, sigma)

    # Application du filtre sur chaque pixel de l'image
    for y in range(pixels.shape[0]):  
        for x in range(pixels.shape[1]): 
            r, g, b = 0, 0, 0  # Initialisation des valeurs de couleur

            # Application du noyau sur la zone entourant le pixel
            for ligne in range(-taille//2, taille//2 + 1):  
                for colonne in range(-taille//2, taille//2 + 1): 
                    pixel_gauss_ligne, pixel_gauss_colonne = y + ligne, x + colonne

                    # Vérification que le pixel est dans les limites de l'image
                    if pixel_gauss_ligne >= 0 and pixel_gauss_ligne < len(pixels) and pixel_gauss_colonne >= 0 and pixel_gauss_colonne < len(pixels[0]):

                        r += pixels[pixel_gauss_ligne, pixel_gauss_colonne, 0] * noyau_final[ligne + taille//2, colonne + taille//2]
                        g += pixels[pixel_gauss_ligne, pixel_gauss_colonne, 1] * noyau_final[ligne + taille//2, colonne + taille//2]
                        b += pixels[pixel_gauss_ligne, pixel_gauss_colonne, 2] * noyau_final[ligne + taille//2, colonne + taille//2]

            # Limiter les valeurs des couleurs entre 0 et 255
            r = min(max(int(r), 0), 255)
            g = min(max(int(g), 0), 255)
            b = min(max(int(b), 0), 255)

            pixels[y, x] = (r, g, b)  # Mise à jour du pixel

    # Création de l'image floutée et renvoi
    image_flouté_gauss = Image.fromarray(pixels)
    return image_flouté_gauss

# Fonction d'interface pour appliquer le flou gaussien
def interface_gaussien(): 
    global dialogue_effet
    dialogue_effet = tk.Toplevel(racine)  # Création d'une nouvelle fenêtre
    dialogue_effet.title("Flou Gaussien")
    dialogue_effet.geometry("400x400")  # Taille de la fenêtre
    dialogue_effet.grab_set()

    label_taille = tk.Label(dialogue_effet, text="Taille du noyau :")
    label_taille.pack(pady=10)

    taille_widget = tk.Scale(dialogue_effet, from_=1, to=15,
                             orient=tk.HORIZONTAL, length=250,
                             resolution=2)  
    taille_widget.set(3)
    taille_widget.pack(pady=10)

    # Label et curseur pour le sigma
    label_sigma = tk.Label(dialogue_effet, text="Sigma :")
    label_sigma.pack(pady=10)

    slider_sigma = tk.Scale(dialogue_effet, from_=0.5, to=5.0,
                            orient=tk.HORIZONTAL, length=250,
                            resolution=0.1, digits=2)
    slider_sigma.set(1.0)
    slider_sigma.pack(pady=10)

    # Frame pour les boutons
    bouton = tk.Frame(dialogue_effet)
    bouton.pack(side=tk.BOTTOM, pady=50)

    # Fonction appliquant le flou gaussien à l'image
    def appliquer_flou():
        taille = taille_widget.get()  # Récupération de la taille du noyau
        sigma = slider_sigma.get()  # Récupération de la valeur de sigma

        if taille % 2 == 0: 
            taille += 1

        
        image_flouter = flou_gaussien(taille, sigma)

        global image_loader  
        image_loader = image_flouter

        
        add_history(image_loader)
        image_canva(canvas, racine)

        
        dialogue_effet.destroy()


    bouton_appliquer = tk.Button(bouton, text="Appliquer",  font=("Arial", 10), bg="#f7dcdc", command=appliquer_flou)
    bouton_appliquer.pack(side=tk.LEFT, padx=7)

    bouton_annuler = tk.Button(bouton, text="Annuler",  font=("Arial", 10), bg="#f7dcdc", command=dialogue_effet.destroy)
    bouton_annuler.pack(side=tk.LEFT, padx=7)


menu_edit.add_command(label="Flou gaussien", command=interface_gaussien)






#FILTRE FUSION

def filtre_de_fusion(alpha):       #(YANN)
    global image, image_loader, image_loader_2

    # if image_loader.size != image_loader_2.size:
    #     image_loader_2 = image_loader_2.resize(image_loader.size)

    image_1 = np.array(image_loader.convert('RGB'))
    image_2 = np.array(image_loader_2.convert('RGB'))

    if image_1.shape != image_2.shape:
        for y in range(image_1.shape[0]):
            for x in range(image_1.shape[1]):
                r = int(image_1[y, x, 0] * alpha + image_2[y, x, 0] * (1 - alpha))
                g = int(image_1[y, x, 1] * alpha + image_2[y, x, 1] * (1 - alpha))
                b = int(image_1[y, x, 2] * alpha + image_2[y, x, 2] * (1 - alpha))
                image_1[y, x] = (r, g, b)
    else:
        a = 1+1
        
    image_loader = Image.fromarray(image_1)
    add_history(image_loader)  
    image_canva(canvas, racine)

    return image_loader


def interface_de_fusion(): 
    global dialogue_effet
    dialogue_effet = tk.Toplevel(racine)  # Création d'une nouvelle fenêtre
    dialogue_effet.title("Fusion d'Images")
    dialogue_effet.geometry("400x400")  
    dialogue_effet.grab_set()

    label_alpha = tk.Label(dialogue_effet, text="Alpha (entre 0.0 et 1.0) :")
    label_alpha.pack(pady=10)

    taille_widget = tk.Scale(dialogue_effet, from_=0.0, to=1.0,
                             orient=tk.HORIZONTAL, length=200,
                             resolution=0.01, digits=2)  
    taille_widget.set(0.5)
    taille_widget.pack(pady=10)
                   

    # Frame pour les boutons
    bouton = tk.Frame(dialogue_effet)
    bouton.pack(side=tk.BOTTOM, pady=50)

    # Fonction appliquant l'image
    def appliquer_fusion():
        alpha = taille_widget.get()   # Récupération de la valeur de sigma 
        
        dialogue_effet.destroy()
        
        image_doubler = filtre_de_fusion(alpha)

        global image_loader  
        image_loader = image_doubler 

        
        add_history(image_loader)
        image_canva(canvas, racine)

        
        dialogue_effet.destroy()


    bouton_appliquer = tk.Button(bouton, text="Appliquer", font=("Arial", 10), bg="#f7dcdc", command=appliquer_fusion)
    bouton_appliquer.pack(side=tk.LEFT, padx=7)

    bouton_annuler = tk.Button(bouton, text="Annuler", font=("Arial", 10), bg="#f7dcdc", command=dialogue_effet.destroy)
    bouton_annuler.pack(side=tk.LEFT, padx=7)


menu_edit.add_command(label="Fusion d'Images", command=interface_de_fusion)

# def interface_de_fusion():
#     global dialogue_effet

#     dialogue_effet = tk.Toplevel(racine)
#     dialogue_effet.title("Fusion d'images")
#     dialogue_effet.geometry("300x200")
#     dialogue_effet.grab_set()

#     label_alpha = tk.Label(dialogue_effet, text="Alpha (0.0 - 1.0) :")
#     label_alpha.grid()
#     slider_alpha = tk.Scale(dialogue_effet, from_=0.0, to=1.0,
#                             orient=tk.HORIZONTAL, length=200,
#                             resolution=0.01, digits=2)
#     slider_alpha.set(0.5)  
#     slider_alpha.grid(pady=10)

    
#     bouton = tk.Frame(dialogue_effet)
#     bouton.grid(side=tk.BOTTOM, pady=20)

#     def appliquer_fusion():
#         alpha = slider_alpha.get() 
#         filtre_de_fusion(alpha)  

#         dialogue_effet.destroy()

#     bouton_appliquer = tk.Button(bouton, text="Appliquer", command=appliquer_fusion)
#     bouton_appliquer.pack(side=tk.LEFT, padx=7)

#     bouton_annuler = tk.Button(bouton, text="Annuler", command=dialogue_effet.destroy)
#     bouton_annuler.pack(side=tk.LEFT, padx=7)


# menu_edit.add_command(label="Fusion d'images", command=interface_de_fusion)   



























































# AIDE quand on decoule la cascade il y a l'entete help document pour afficher le 2e canvas 


menu_aide = tk.Menu(menu_principal, tearoff=0)                  
menu_principal.add_cascade(label="Aide", menu=menu_aide)           


def fichier_help():          # ici on a cree une autre fenetre canvas par dessus le canvas de base pour expliquer les differentes fonctionnaliter des filtres par ex 
    global aide              

    aide = tk.Canvas(racine, width=950, height=800, bg='white')
    aide.grid(row=0, column=0)

    # Texte et bouton
    aide.create_text(350, 260, text="ici on explique les filtres ect pour aider l'utilisateur", font=("Helvetica", 10, "bold"), fill='black')
    aide.create_window(350, 320, window=tk.Menu(aide, text="ici on explique les filtres ect pour aider l'utilisateur", font=("Helvetica", 10, "bold"), command=fichier_help))

menu_aide.add_command(label="Help document", command=fichier_help)







racine.mainloop()

 