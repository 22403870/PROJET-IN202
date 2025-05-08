import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import pathlib
import time
import math
from scipy.signal import convolve2d

global image_history_filters , image_history_redo, image_save
image_history_filters = []
image_history_redo = [] #si on veut remettre la photo comme elle etait avant le Redo
canvas_created = False
image_save = ''

def add_history(image):
	image_history_filters.append(np.array(image))

def open_file(background_canva , uvsq_root , image_name = 'modified_image.jpg'):
	global file_opened , image_loader , image
	file_opened = str(tk.filedialog.askopenfilename())
	image_loader = Image.open(str(file_opened))
	image_loader.save(image_name)
	image_loader = image_loader.convert("RGB")
	image_history_filters.append(np.array(image_loader))
	uvsq_root.title( file_opened)
	image_canva(background_canva, uvsq_root)

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

def average_pix(pixel):
	r,g,b = pixel
	return (r+g+b)//3

def get_pixel_rgb(x, y,image = ''):
	if image == '':
		image=image_loader
	return image.getpixel((x, y))

def image_path(image_name):
	return f'{pathlib.Path(__file__).parent.resolve()}/{image_name}'

def apply_filter(background_canva , uvsq_root, image_name = 'modified_image.jpg' , image_redo = False):
	global image , image_loader , image_history_redo
	image_loader = Image.open(image_path(image_name))
	add_history(np.array(image_loader.convert("RGB")))
	if not image_redo:
		image_history_redo = []
	image_canva(background_canva , uvsq_root)

def green_filter(uvsq_root , image_name = 'modified_image.jpg'):
	global image , image_loader
	image = Image.open(file_opened)
	image = image.convert('RGB')
	pixels = np.array(image)
	for pixel_y in range(len(pixels)):
		for pixel_x in range(len(pixels[pixel_y])):
			average = average_pix(get_pixel_rgb(pixel_x , pixel_y))
			image.putpixel((pixel_x , pixel_y), (0,average,0))
	image.save(image_name)
	apply_filter(canvas_used , uvsq_root , image_name)

def red_filter(uvsq_root , image_name = 'modified_image.jpg'):
	global image , image_loader
	image = Image.open(file_opened)
	image = image.convert('RGB')
	pixels = np.array(image)
	for pixel_y in range(len(pixels)):
		for pixel_x in range(len(pixels[pixel_y])):
			average = average_pix(get_pixel_rgb(pixel_x , pixel_y))
			image.putpixel((pixel_x , pixel_y), (average,0,0))
	image.save(image_name)
	apply_filter(canvas_used , uvsq_root , image_name)

def blue_filter(uvsq_root , image_name = 'modified_image.jpg'):
	image = Image.open(file_opened)
	image = image.convert('RGB')
	pixels = np.array(image)
	for pixel_y in range(len(pixels)):
		for pixel_x in range(len(pixels[pixel_y])):
			average = average_pix(get_pixel_rgb(pixel_x , pixel_y))
			image.putpixel((pixel_x , pixel_y), (0,0,average))
	image.save(image_name)
	apply_filter(canvas_used , uvsq_root , image_name)

def gray_filter(uvsq_root , image_name = "modified_image.jpg"):
	global image , image_loader
	image = Image.open(file_opened)
	image = image.convert('RGB')
	pixels = np.array(image)
	for pixel_y in range(len(pixels)):
		for pixel_x in range(len(pixels[pixel_y])):
			average = average_pix(get_pixel_rgb(pixel_x , pixel_y))
			image.putpixel((pixel_x , pixel_y), (average,average,average))
	image.save(image_name)
	apply_filter(canvas_used , uvsq_root , image_name)

def no_efect(root):
	global image , image_loader
	image_loader = Image.open(file_opened)
	image_canva(canvas_used , root)

def contrast(slider_1 , slider_2 , uvsq_root , image_name = 'modified_image.jpg'):
	global image , image_loader
	slider_1 = slider_1.get()
	slider_2 = slider_2.get()
	def contrast_sigma(canal):
		contrast_average = (canal//255)
		exponent = -(slider_2*(contrast_average - slider_1))
		contrast_sigma_canal = 1 / ( 1 + math.exp(exponent))
		return int(contrast_sigma_canal*canal)

	image = Image.open(file_opened)
	image = image.convert('RGB')
	pixels = np.array(image)
	for pixel_y in range(len(pixels)):
		for pixel_x in range(len(pixels[pixel_y])):
			pix = pixels[pixel_y][pixel_x]
			image.putpixel((pixel_x , pixel_y), (
				contrast_sigma(int(pix[0])),
				contrast_sigma(int(pix[1])),
				contrast_sigma(int(pix[2]))))
	image.save(image_name)
	apply_filter(canvas_used , uvsq_root , image_name)

def reverse_rgb(uvsq_root , image_name = 'modified_image.jpg'):
	global image , image_loader
	image = Image.open(file_opened)
	image = image.convert('RGB')
	pixels = np.array(image)
	for pixel_y in range(len(pixels)):
		for pixel_x in range(len(pixels[pixel_y])):
			pixel_r , pixel_g , pixel_b = get_pixel_rgb(pixel_x , pixel_y)
			image.putpixel((pixel_x , pixel_y), (255-pixel_r,255-pixel_g,255-pixel_b))
	image.save(image_name)
	apply_filter(canvas_used , uvsq_root, image_name)


def fusion_image(uvsq_root , image_name = 'modified_image.jpg' ):
	global image , image_loader
	image_2 = Image.open(str(tk.filedialog.askopenfilename()))
	image = Image.open(file_opened)
	image = image.convert('RGB')
	array_image = [np.array(image) , np.array(image_2.convert("RGB"))]
	for pixel_y in range(len(array_image[0])):
		for pixel_x in range(len(array_image[0][pixel_y])):
			pixel_r , pixel_g , pixel_b = np.add(get_pixel_rgb(pixel_x , pixel_y , image) , get_pixel_rgb(pixel_x , pixel_y , image_2))
			image.putpixel((pixel_x , pixel_y),(pixel_r//2,pixel_g//2,pixel_b//2))

	image.save(image_name)
	apply_filter(canvas_used , uvsq_root, image_name)

def reverse_photo(uvsq_root , image_name = 'modified_image.jpg'):
	image = Image.open(image_path(image_name))
	image = image.convert('RGB')
	pixel_matrix = np.array(image)
	for pixel_y in range(len(pixel_matrix)):
		for pixel_x in range(len(pixel_matrix[pixel_y])):
			image.putpixel((pixel_x , pixel_y),(pixel_matrix[pixel_y][len(pixel_matrix[pixel_y])-1-pixel_x][0],
			pixel_matrix[pixel_y][len(pixel_matrix[pixel_y])-1-pixel_x][1],
			pixel_matrix[pixel_y][len(pixel_matrix[pixel_y])-1-pixel_x][2]))
	image.save(image_name)
	apply_filter(canvas_used , uvsq_root)

def correction_gamma(slider,uvsq_root, image_name = 'modified_image.jpg'):
	slider = slider.get()
	def calculate_gamma(slider , pixel):
		pixel_r , pixel_g , pixel_b = pixel
		return int(pixel_r*(slider)) , int(pixel_g*(slider)) , int(pixel_b*(slider))
	global image , image_loader
	image = Image.open(file_opened)
	image = image.convert('RGB')
	pixels = np.array(image)
	for pixel_y in range(len(pixels)):
		for pixel_x in range(len(pixels[pixel_y])):
			gamme_r,gamma_g,gamma_b = calculate_gamma(slider,get_pixel_rgb(pixel_x , pixel_y))
			image.putpixel((pixel_x , pixel_y), (gamme_r,gamma_g,gamma_b))
	image.save(image_name)
	apply_filter(canvas_used , uvsq_root, image_name)


def save_image(uvsq_root ,image_name = 'modified_image.jpg'):

	if file_opened != '':
		image = Image.open(image_path(image_name))
	if image_save =='':
		image.save(file_opened)
	else:
		image.save(image_save)

def save_image_as(uvsq_root ,image_name = 'modified_image.jpg'):
	if file_opened != '':
		image_save = tk.filedialog.asksaveasfilename(filetypes=[("PNG files", "*.png"),
                                                          ("JPEG files", "*.jpg;*.jpeg"),
                                                          ("Bitmap files", "*.bmp"),
                                                          ("GIF files", "*.gif")])
		image = Image.open(image_path(image_name))
		image.save(image_save)
		uvsq_root.title(image_save)

def undo(uvsq_root ,image_name = 'modified_image.jpg'):
	if len(image_history_filters) >1:
		image_history_redo.append(image_history_filters.pop())
		image_undo = image_history_filters.pop()
		image = Image.open(file_opened)
		image = image.convert('RGB')
		pixels = np.array(image)
		for pixel_y in range(len(pixels)):
			for pixel_x in range(len(pixels[pixel_y])):
				image.putpixel((pixel_x , pixel_y), tuple([int(canal) for canal in image_undo[pixel_y][pixel_x]]))
		image.save(image_name)
		apply_filter(canvas_used , uvsq_root , image_redo = True)


def redo(uvsq_root ,image_name = 'modified_image.jpg'):
	if len(image_history_redo) > 0:
		image_redo = image_history_redo.pop(0)
		image = Image.open(file_opened)
		image = image.convert('RGB')
		pixels = np.array(image)
		for pixel_y in range(len(pixels)):
			for pixel_x in range(len(pixels[pixel_y])):
				image.putpixel((pixel_x , pixel_y), tuple([int(canal) for canal in image_redo[pixel_y][pixel_x]]))
		image.save(image_name)
		apply_filter(canvas_used , uvsq_root , image_redo = True)

def blur(bluring_size , bluring_strenght , uvsq_root ,image_name = 'modified_image.jpg'):
	bluring_strenght = int(bluring_strenght.get())
	bluring_size = int(bluring_size.get())

	image = Image.open(image_name)
	image = image.convert('RGB')
	pixels = np.array(image)
	def gaussian_kernel(size, sigma = 1):
		kernel = np.fromfunction( lambda x, y: (1/ (2 * np.pi * sigma**2)) * np.exp(-((x - (size - 1) / 2)**2 + (y - (size - 1) / 2)**2) / (2 * sigma**2)),(size, size))
		return kernel / np.sum(kernel)

	kernel = gaussian_kernel(bluring_size , bluring_strenght)
	canal_red = convolve2d(pixels[:,:,0], kernel, mode = 'same' , boundary = 'symm')
	canal_green = convolve2d(pixels[:,:,1], kernel, mode = 'same' , boundary = 'symm')
	canal_blue = convolve2d(pixels[:,:,2], kernel, mode = 'same' , boundary = 'symm')


	blurred_image = np.stack((canal_red, canal_green, canal_blue), axis=-1)
	for pixel_y in range(len(blurred_image)):
		for pixel_x in range(len(blurred_image[pixel_y])):
			image.putpixel((pixel_x , pixel_y), tuple([int(canal) for canal in blurred_image[pixel_y][pixel_x]]))


	image.save(image_name)
	apply_filter(canvas_used , uvsq_root, image_name)
