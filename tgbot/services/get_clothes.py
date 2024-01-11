import random

from tgbot.database import db_clothes
from tgbot.models.SetClothes import SetClothes, ElClothes, ElBody
from tgbot.models.SimpleWeather import SimpleWeather


def get_clothes(simple_weather: SimpleWeather):
	# изучить что надеть!
	# head, body, legs, shoes, accessories = str


	head = get_head(simple_weather)
	body = get_body(simple_weather)
	legs = get_legs(simple_weather)
	shoes = get_shoes(simple_weather)
	accessories = get_accessories(simple_weather)


	set_clothes = SetClothes(head=head, body=body, legs=legs, shoes=shoes, accessories=accessories)

	return set_clothes


def get_head(simple_weather: SimpleWeather):
	heads = db_clothes.get_head_sql()
	head = ['', '']
	# голова:
	if float(simple_weather.cur_weather) <= 0:
		heads = [x for x in heads if int(x[4]) >= 2]
		head = random.choice(heads)

	if simple_weather.weather_description == "Ясно☀️" and float(simple_weather.cur_weather) > 13:
		heads = db_clothes.get_head_sql()
		heads = [x for x in heads if x[3] == 'лето_солнце']
		head = random.choice(heads)

	el_head = ElClothes(name=head[1], img=head[-1])

	return el_head


def get_body(simple_weather: SimpleWeather):
	bodys = db_clothes.get_body_sql()
	_outer_body = None
	_under_body = None
	under_body = ElClothes(name="", img="")
	outer_body = ElClothes(name="", img="")

	under_bodys = [x for x in bodys if not (x[3].startswith("верхнее") or x[3].startswith("нижнее"))]
	print("under_bodys ", under_bodys)

	if  0 < float(simple_weather.cur_weather) < 10:
		outer_bodys = [x for x in bodys if x[3].startswith("верхнее_осень")]
		_outer_body = random.choice(outer_bodys)
	if  float(simple_weather.cur_weather) <= 0:
		outer_bodys = [x for x in bodys if x[3].startswith("верхнее_зима")]
		_outer_body = random.choice(outer_bodys)
		print('outer_bodys', outer_bodys)
	if  float(simple_weather.cur_weather) > 0 and (simple_weather.weather_description == "Дождь🌦" or simple_weather.weather_description == "Гроза🌩" or simple_weather.weather_description == "Ливень🌧"):
		outer_bodys = [x for x in bodys if x[3].startswith("верхнее_дождь")]
		_outer_body = random.choice(outer_bodys)


	if float(simple_weather.cur_weather) >= 15:
		under_bodys = [x for x in bodys if x[3].startswith("лето") or x[3].startswith("-")]
		under_bodys = [x for x in under_bodys if int(x[4]) == 1]
		_under_body = random.choice(under_bodys)

	if 10 <= float(simple_weather.cur_weather) < 15:
		under_bodys = [x for x in bodys if x[3].startswith("осень") or x[3].startswith("-")]
		under_bodys = [x for x in under_bodys if int(x[4]) <= 2]
		_under_body = random.choice(under_bodys)

	if 0 <= float(simple_weather.cur_weather) < 10:
		under_bodys = [x for x in bodys if x[3].startswith("осень") or x[3].startswith("зима") or x[3].startswith("-")]
		under_bodys = [x for x in under_bodys if int(x[4]) <= 4]
		_under_body = random.choice(under_bodys)

	if -10 <= float(simple_weather.cur_weather) < 0:
		under_bodys = [x for x in bodys if x[3].startswith("зима") or x[3].startswith("-")]
		under_bodys = [x for x in under_bodys if int(x[4]) <= 5]
		_under_body = random.choice(under_bodys)

	if -15 <= float(simple_weather.cur_weather) < -10:
		under_bodys = [x for x in bodys if x[3].startswith("зима") or x[3].startswith("-")]
		under_bodys = [x for x in under_bodys if int(x[4]) <= 5]
		_under_body = random.choice(under_bodys)

	if float(simple_weather.cur_weather) < -15:
		under_bodys = [x for x in under_bodys if int(x[4]) >= 3]
		_under_body = random.choice(under_bodys)

	if _outer_body:
		outer_body = ElClothes(name=_outer_body[1], img=_outer_body[-1])

	if not _under_body:
		_under_body = random.choice(under_bodys)

	print("_under_body ", _under_body)
	under_body = ElClothes(name=_under_body[1], img=_under_body[-1])

	el_body = ElBody(outerwear=outer_body, underwear=under_body)

	return el_body


def get_legs(simple_weather: SimpleWeather):
	legs = db_clothes.get_legs_sql()

	# ноги:
	if 15 <= float(simple_weather.cur_weather):
		legs = [x for x in legs if int(x[4]) < 2]
		legs_favorite = random.choice(legs)
	if 15 > float(simple_weather.cur_weather) >= 0:
		legs = [x for x in legs if int(x[4]) >= 2]
		legs_favorite = random.choice(legs)
	if float(simple_weather.cur_weather) < 0:
		legs = [x for x in legs if int(x[4]) >= 3]
		legs_favorite = random.choice(legs)

	el_legs = ElClothes(name=legs_favorite[1], img=legs_favorite[-1])

	return el_legs


def get_shoes(simple_weather: SimpleWeather):
	shoes = db_clothes.get_shoes_sql()

	# ботинки:
	if simple_weather.weather_description == "Дождь🌦":
		shoes = [x for x in shoes if x[3].startswith("дождь")]
		shoes_favorite = random.choice(shoes)
	else:
		if float(simple_weather.cur_weather) >= 20:
			shoes = [x for x in shoes if int(x[4]) == 1]
			shoes_favorite = random.choice(shoes)

		if 0 <= float(simple_weather.cur_weather) < 20:
			shoes = [x for x in shoes if int(x[4]) == 2]
			shoes_favorite = random.choice(shoes)

		if -10 <= float(simple_weather.cur_weather) < 0:
			shoes = [x for x in shoes if int(x[4]) == 3]
			shoes_favorite = random.choice(shoes)

		if -25 <= float(simple_weather.cur_weather) < -10:
			shoes = [x for x in shoes if int(x[4]) == 4]
			shoes_favorite = random.choice(shoes)

		if float(simple_weather.cur_weather) < -25:
			shoes = [x for x in shoes if int(x[4]) == 5]
			shoes_favorite = random.choice(shoes)

	el_shoes = ElClothes(name=shoes_favorite[1], img=shoes_favorite[-1])

	return el_shoes


def get_accessories(simple_weather: SimpleWeather):
	accessories = db_clothes.get_accessories_sql()
	accessories_favorite = []
	res = []

	# аксессуары:
	if float(simple_weather.cur_weather) < -15:
		_accessories = [x for x in accessories if x[2].startswith("ступни_нижнее") and int(x[4]) >= 3]
		accessories_favorite.append(random.choice(_accessories))

	if float(simple_weather.cur_weather) <= 0:
		_accessories = [x for x in accessories if x[2].startswith("руки") and int(x[4]) >= 2]
		accessories_favorite.append(random.choice(_accessories))

	for accessorie in accessories_favorite:
		el_accessories = ElClothes(name=accessorie[1], img=accessorie[-1])
		res.append(el_accessories)

	return res