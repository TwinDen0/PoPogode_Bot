import random
from typing import List

from PIL import Image, ImageDraw, ImageFont
from aiofiles import os


def img_layering(image, watermark, position):
	layer = Image.new('RGBA', image.size, (255, 255, 255))
	layer.paste(image, (0, 0))
	layer.paste(watermark, (int(position[0]), int(position[1])))
	return Image.composite(layer, image, layer)

def clothes_layering(head = None, outerwear = None, underwear = None, undies = None, legs = None, shoes = None, accessories = None):
	imgs = []
	clts = []

	coord_imgs = []
	coord_clts = []

	if accessories or head:
		dop = "+ac"
	else:
		dop = ""

	count_cloth = 0
	cloths = [outerwear, underwear, undies, legs]
	for i in cloths:
		if i:
			count_cloth += 1

	base = f"./tgbot/img/fon_{count_cloth}{dop}.png"

	#             штаны      ботинки    тело_нижняя
	coord_clts = [[34, 255], [54, 326],  [34, 138]]
	if head:
		coord_clts.append([65, -2])
	#тело_вверхняя
	coord_clts.append([34, 138])
	#акссесуары
	coord_clts.append([65, -2])
	coord_clts.append([65, -2])

	#             тело_вверхняя   тело_нижняя                штаны
	# coord_imgs = [[281, 91],      [531, 91],     [870, 91], [65, 0]]
	# coord_imgs = [[281, 91], [281, 91], [281, 91], [281, 91], [281, 91], [281, 91]]

	coord_imgs.append([281, 91])
	if outerwear:
		coord_imgs.append([531, 91])
	if undies:
		coord_imgs.append([870, 91])
	if count_cloth == 2:
		coord_imgs.append([493, 91])
	elif count_cloth == 3:
		coord_imgs.append([740, 91])
	elif count_cloth == 4:
		coord_imgs.append([950, 91])

	for i in range(0, 5):
		if count_cloth == 2:
			coord_imgs.append([700, 91])
		elif count_cloth == 3:
			coord_imgs.append([950, 91])
		elif count_cloth == 4:
			coord_imgs.append([1150, 91])



	base = Image.open(base).convert("RGBA")

	clts.append(Image.open(f'./tgbot/img/{legs}_2.png').convert("RGBA"))
	clts.append(Image.open(f'./tgbot/img/{shoes}.png').convert("RGBA"))
	clts.append(Image.open(f'./tgbot/img/{underwear}_2.png').convert("RGBA"))

	if head:
		clts.append(Image.open(f'./tgbot/img/{head}_2.png').convert("RGBA"))

	if outerwear:
		clts.append(Image.open(f'./tgbot/img/{outerwear}_2.png').convert("RGBA"))
		imgs.append(Image.open(f'./tgbot/img/{outerwear}_1.png').convert("RGBA"))

	imgs.append(Image.open(f'./tgbot/img/{underwear}_1.png').convert("RGBA"))
	if undies:
		imgs.append(Image.open(f'./tgbot/img/{undies}_1.png').convert("RGBA"))
	imgs.append(Image.open(f'./tgbot/img/{legs}_1.png').convert("RGBA"))

	if len(accessories) > 0:
		for acces in accessories:
			try:
				clts.append(Image.open(f'./tgbot/img/{acces.img}_2.png').convert("RGBA"))

			except:
				pass

		imgs.append(Image.open(f'./tgbot/img/{accessories[-1].img}_1.png').convert("RGBA"))

	elif head:
		imgs.append(Image.open(f'./tgbot/img/{head}_1.png').convert("RGBA"))

	for i in range(0, len(imgs)):
		x = coord_imgs[i][0]
		y = coord_imgs[i][1]

		if i == 0:
			result = img_layering(base, imgs[i], (x, y))
		else:
			result = img_layering(result, imgs[i], (x, y))

	for i in range(0, len(clts)):
		x = coord_clts[i][0]
		y = coord_clts[i][1]

		result = img_layering(result, clts[i], (x, y))


	new_path = './tgbot/img/' + str(random.randint(1, 10000000)) + '.jpg'
	result = result.convert("RGB")
	result.save(new_path, format="JPEG")

	return new_path

def layering_array(imgs=[]):
	coord = []
	for img in imgs:
		if type(img) == list and type(img[1]) == int and type(img[2]) == int:
			x = img[1]
			y = img[2]
		else:
			x = 0
			y = 0
		coord.append([x, y])
	coord.append([0, 0])
	layers = []
	for img in imgs:
		if type(img) == list:
			if type(img[0]) == str:
				layer = Image.open(img[0]).convert("RGBA")
			else:
				layers.append(img[0])
		else:
			if type(img) != str:
				layers.append(img)
		if type(img) == str:
			layer = Image.open(img).convert("RGBA")
			layers.append(layer)

	for i in range(0, len(layers)):
		x = coord[i + 1][0]
		y = coord[i + 1][1]
		if i == 0 and len(layers) > 1:
			result = img_layering(layers[i], layers[i + 1], (x, y))
		elif len(layers) != i + 1:
			result = img_layering(result, layers[i + 1], (x, y))
		elif len(layers) == 1:
			result = layers[i]

	return result
