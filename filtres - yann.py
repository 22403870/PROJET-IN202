
def filtre_vert():
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

###

def noyau_filtre_gauss(taille, sigma):

    noyau = np.zeros((taille, taille))
    pixel_principale = taille // 2

    for i in range(taille):
        for j in range(taille):
            x = i - pixel_principale
            y = j - pixel_principale
            noyau[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    noyau /= np.sum(noyau)

    return noyau

def flou_gaussien(taille, sigma):
    global image, image_loader

    pixels = np.array(image_loader.convert('RGB'))

    noyau_final = noyau_filtre_gauss(taille, sigma)
   

    for y in range(pixels.shape[0]):  
        for x in range(pixels.shape[1]): 
            r, g, b = 0, 0, 0 
            
            for ligne in range(-taille//2, taille//2 + 1):  
                for colonne in range(-taille//2, taille//2 + 1): 
                    pixel_gauss_ligne, pixel_gauss_colonne = y + ligne, x + colonne

                    if pixel_gauss_ligne >= 0 and pixel_gauss_ligne < len(pixels) and pixel_gauss_colonne >= 0 and pixel_gauss_colonne < len(pixels[0]):

                        r += pixels[pixel_gauss_ligne, pixel_gauss_colonne, 0] * noyau_final[ligne + taille//2, colonne + taille//2]
                        g += pixels[pixel_gauss_ligne, pixel_gauss_colonne, 1] * noyau_final[ligne + taille//2, colonne + taille//2]
                        b += pixels[pixel_gauss_ligne, pixel_gauss_colonne, 2] * noyau_final[ligne + taille//2, colonne + taille//2]

            pixels[y, x] = (int(r), int(g), int(b))

    image_flouté_gauss = Image.fromarray(pixels)
    return image_flouté_gauss

def interface_gaussien(): 
    global dialogue_effet
    dialogue_effet = tk.Toplevel(racine)
    dialogue_effet.title("Flou Gaussien")
    dialogue_effet.geometry("300x150")
    dialogue_effet.grab_set()

    
    label_taille = tk.Label(dialogue_effet, text="taille du noyau :")
    label_taille.pack()
    taille = tk.Scale(dialogue_effet, from_=1, to=15,
                             orient=tk.HORIZONTAL, length=200,
                             resolution=2)  
    taille.set(3)
    taille.pack(pady=10)

   
    label_sigma = tk.Label(dialogue_effet, text="Sigma :")
    label_sigma.pack()
    slider_sigma = tk.Scale(dialogue_effet, from_=0.5, to=5.0,
                            orient=tk.HORIZONTAL, length=200,
                            resolution=0.1, digits=2)
    slider_sigma.set(1.0)
    slider_sigma.pack(pady=10)

    bouton = tk.Frame(dialogue_effet)
    bouton.pack(side=tk.BOTTOM, pady=10)

    def appliquer_flou():
        taille = taille.get()
        sigma = slider_sigma.get()

        if taille % 2 == 0:
            taille += 1

        image_flouter = flou_gaussien(taille, sigma)

        global image_loader
        image_loader = image_flouter

        add_history(image_loader)
        image_canva(canvas, racine)

        dialogue_effet.destroy()

    bouton_appliquer = tk.Button(bouton, text="Appliquer", command=appliquer_flou)
    bouton_appliquer.pack(side=tk.LEFT, padx=10)

    bouton_annuler = tk.Button(bouton, text="Annuler", command=dialogue_effet.destroy)
    bouton_annuler.pack(side=tk.LEFT, padx=10)

menu_edit.add_command(label="Flou Gaussien", command=interface_gaussien)

###

def filtre_de_fusion(alpha):
    global image, image_loader, image_loader_2

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


def interface_de_fusion():
    global dialogue_effet

    dialogue_effet = Toplevel(racine)
    dialogue_effet.title("Fusion d'images")
    dialogue_effet.geometry("300x200")
    dialogue_effet.grab_set()

    label_alpha = tk.Label(dialogue_effet, text="Alpha (0.0 - 1.0) :")
    label_alpha.pack()
    slider_alpha = tk.Scale(dialogue_effet, from_=0.0, to=1.0,
                            orient=tk.HORIZONTAL, length=200,
                            resolution=0.01, digits=2)
    slider_alpha.set(0.5)  
    slider_alpha.pack(pady=10)

    
    bouton = tk.Frame(dialogue_effet)
    bouton.pack(side=tk.BOTTOM, pady=10)

    def appliquer_fusion():
        alpha = slider_alpha.get() 
        filtre_de_fusion(alpha)  

        dialogue_effet.destroy()

    bouton_appliquer = tk.Button(bouton, text="Appliquer", command=appliquer_fusion)
    bouton_appliquer.pack(side=tk.LEFT, padx=10)

    bouton_annuler = tk.Button(bouton, text="Annuler", command=dialogue_effet.destroy)
    bouton_annuler.pack(side=tk.LEFT, padx=10)

menu_edit.add_command(label="Fusion d'images", command=interface_de_fusion)   