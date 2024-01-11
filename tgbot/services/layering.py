import random
from typing import List

from PIL import Image, ImageDraw, ImageFont

def img_layering(image, watermark, position):
	layer = Image.new('RGBA', image.size, (255, 255, 255))
	layer.paste(image, (0, 0))
	layer.paste(watermark, (int(position[0]), int(position[1])))
	return Image.composite(layer, image, layer)

def clothes_layering(outerwear = None, underwear = None, undies = None, legs = None, shoes = None, accessories = None):
	imgs = []
	clts = []

	coord_imgs = [[520, 65], [260, 65]]
	coord_clts = [[55, 228], [55, 118]]

	if accessories:
		dop = "+ac"
	else:
		dop = ""

	if outerwear and underwear and undies:
		base = f"./tgbot/img/fon_4{dop}.png"
		#             тело_нижняя   тело_вверхняя                штаны
		coord_imgs = [[281, 91],    [531, 91],       [781, 91], [994, 91], [1000, 1000]]
		#             штаны      ботинки     тело_нижняя   тело_вверхняя    голова
		coord_clts = [[34, 255], [55, 326],  [34, 138],   [34, 138],       [1000, 1000]]
	if (outerwear and underwear and not undies) or (underwear and undies and not outerwear):
		base = f"./tgbot/img/fon_3{dop}.png"
		#             тело_нижняя   тело_вверхняя                штаны
		coord_imgs = [[281, 91],    [531, 91],       [781, 91], [994, 91], [1000, 1000]]
		#             штаны      ботинки     тело_нижняя   тело_вверхняя    голова
		coord_clts = [[34, 255], [55, 326],  [34, 138],   [34, 138],       [1000, 1000]]
	if underwear and not outerwear and not undies:
		base = f"./tgbot/img/fon_2{dop}.png"
		#             тело_нижняя   тело_вверхняя                штаны
		coord_imgs = [[281, 91],    [531, 91],       [781, 91], [994, 91], [1000, 1000]]
		#             штаны      ботинки     тело_нижняя   тело_вверхняя    голова
		coord_clts = [[34, 255], [55, 326],  [34, 138],   [34, 138],       [1000, 1000]]


	base = Image.open(base).convert("RGBA")

	clts.append(Image.open(f'./tgbot/img/{legs}_2.png').convert("RGBA"))
	clts.append(Image.open(f'./tgbot/img/{shoes}.png').convert("RGBA"))
	clts.append(Image.open(f'./tgbot/img/{underwear}_2.png').convert("RGBA"))
	if outerwear:
		clts.append(Image.open(f'./tgbot/img/{outerwear}_2.png').convert("RGBA"))

	if outerwear:
		imgs.append(Image.open(f'./tgbot/img/{outerwear}_1.png').convert("RGBA"))
	imgs.append(Image.open(f'./tgbot/img/{underwear}_1.png').convert("RGBA"))
	if undies:
		imgs.append(Image.open(f'./tgbot/img/{undies}_1.png').convert("RGBA"))
	imgs.append(Image.open(f'./tgbot/img/{legs}_1.png').convert("RGBA"))


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
