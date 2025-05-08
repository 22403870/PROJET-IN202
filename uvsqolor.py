import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import pathlib
import time
import math
from scipy.signal import convolve2d
import effects_uvsqolor as eff

global  image_loader , image , filtre , geometry , file_opened , image_history_filters
file_opened = None # verifie qu'on a bien ouvert un fichier

uvsq_root = tk.Tk()
uvsq_root.geometry("1920x1080")

def bluring():
	def reset_value():
		eff.undo(uvsq_root)

	global dialogue_effet
	dialogue_effet = tk.Toplevel(uvsq_root)
	dialogue_effet.title("Bluring")
	dialogue_effet.geometry("300x300")
	dialogue_effet.grab_set()
	slider = tk.Scale(dialogue_effet, from_=1, to=10,
	                  orient=tk.HORIZONTAL, length=200,
	                  resolution=0.1, digits=2,
	                  )
	slider.set(1.0)
	slider.pack(pady=20)

	sigma_slide = tk.Scale(dialogue_effet, from_=1, to=10,
	                  orient=tk.HORIZONTAL, length=200,
	                  resolution=0.1, digits=2,
	                  )
	sigma_slide.set(1.0)
	sigma_slide.pack(pady=20)

	frame_boutons = tk.Frame(dialogue_effet)
	frame_boutons.pack(side=tk.BOTTOM, pady=10)

	bouton_appliquer = tk.Button(frame_boutons, text="Appliquer",
		command = lambda : eff.blur(slider, sigma_slide  , uvsq_root)
	                             )
	bouton_appliquer.pack(side=tk.LEFT, padx=10)

	bouton_annuler = tk.Button(frame_boutons, text="Annuler",
		command = lambda : reset_value(),
	                           )
	bouton_annuler.pack(side=tk.LEFT, padx=10)

def luminosity():
	def reset_value():
		slider.set(1.0)
		eff.correction_gamma(slider , uvsq_root)

	global dialogue_effet
	dialogue_effet = tk.Toplevel(uvsq_root)
	dialogue_effet.title("Luminosité")
	dialogue_effet.geometry("300x150")
	dialogue_effet.grab_set()
	slider = tk.Scale(dialogue_effet, from_=0.1, to=3.0,
	                  orient=tk.HORIZONTAL, length=200,
	                  resolution=0.1, digits=2,
	                  )
	slider.set(1.0)
	slider.pack(pady=20)

	frame_boutons = tk.Frame(dialogue_effet)
	frame_boutons.pack(side=tk.BOTTOM, pady=10)

	bouton_appliquer = tk.Button(frame_boutons, text="Appliquer",
		command = lambda : eff.correction_gamma(slider, uvsq_root)
	                             )
	bouton_appliquer.pack(side=tk.LEFT, padx=10)

	bouton_annuler = tk.Button(frame_boutons, text="Annuler",
		command = lambda : reset_value(),
	                           )
	bouton_annuler.pack(side=tk.LEFT, padx=10)

def constrast():
	def reset_value():
		slider_1.set(0)
		slider_2.set(0)
		eff.no_efect(uvsq_root)

	global dialogue_effet
	dialogue_effet = tk.Toplevel(uvsq_root)
	dialogue_effet.title("Contrast")
	dialogue_effet.geometry("300x300")
	dialogue_effet.grab_set()

	slider_1 = tk.Scale(dialogue_effet, from_=-1.0, to=1.0,
	                  orient=tk.HORIZONTAL, length=200,
	                  resolution=0.1, digits=2,
	                  )
	slider_1.set(1.0)
	slider_1.pack(pady=20)

	slider_2 = tk.Scale(dialogue_effet, from_=0.1, to= 20.0,
	                  orient=tk.HORIZONTAL, length=200,
	                  resolution=0.1, digits=2,
	                  )
	slider_2.set(1.0)
	slider_2.pack(pady=20)

	frame_boutons = tk.Frame(dialogue_effet)
	frame_boutons.pack(side=tk.BOTTOM, pady=10)

	bouton_appliquer = tk.Button(frame_boutons, text="Appliquer",
		command = lambda : eff.contrast(slider_1,slider_2 ,uvsq_root)
	                             )
	bouton_appliquer.pack(side=tk.LEFT, padx=10)

	bouton_annuler = tk.Button(frame_boutons, text="Annuler",
		command = lambda : reset_value(),
	                           )
	bouton_annuler.pack(side=tk.LEFT, padx=10)


menu_uvsq = tk.Menu(uvsq_root , tearoff=False)
uvsq_root.config(menu=menu_uvsq )
menu_fichier = tk.Menu(menu_uvsq, tearoff=False)
menu_efets = tk.Menu(menu_uvsq , tearoff=False)

menu_uvsq.add_cascade(
    label="fichiers",
    menu=menu_fichier,
    underline=0
)

menu_uvsq.add_cascade(
    label="efets",
    menu=menu_efets,
    underline=0
)

menu_fichier.add_command(label = 'Ouvrir' , command = lambda: eff.open_file(background_canva , uvsq_root))
menu_fichier.add_command(label = 'Save' , command = lambda : eff.save_image(uvsq_root))
menu_fichier.add_command(label = 'Save as' ,command = lambda: eff.save_image_as(uvsq_root))
menu_fichier.add_command(label = 'Undo' ,command = lambda: eff.undo(uvsq_root))
menu_fichier.add_command(label = 'Redo' , command = lambda: eff.redo(uvsq_root))
menu_efets.add_command(label = 'Fusion image' ,  command = lambda: eff.fusion_image(uvsq_root))
menu_efets.add_command(label = 'Efet vert', command = lambda: eff.green_filter(uvsq_root))
menu_efets.add_command(label = 'Efet rouge', command = lambda: eff.red_filter(uvsq_root))
menu_efets.add_command(label = 'Efet blue', command = lambda: eff.blue_filter(uvsq_root))
menu_efets.add_command(label='original' , command = lambda: eff.no_efect(uvsq_root))
menu_efets.add_command(label='efet gris' , command= lambda: eff.gray_filter(uvsq_root))
menu_efets.add_command(label='colors invers' , command= lambda: eff.reverse_rgb(uvsq_root))
menu_efets.add_command(label='luminosity' , command = luminosity)
menu_efets.add_command(label='contrast' , command = constrast)
menu_efets.add_command(label='Blur' , command = bluring)
menu_efets.add_command(label='Flip' , command = lambda:eff.reverse_photo(uvsq_root))

background_canva = tk.Canvas(uvsq_root)
background_canva.pack(expand = True , fill = "both")

if '__main__' ==__name__:
	uvsq_root.mainloop()
