import random

from tgbot.database import db_clothes
from tgbot.models.SetClothes import SetClothes, ElClothes, ElBody
from tgbot.models.SimpleWeather import SimpleWeather


def get_clothes(simple_weather: SimpleWeather):
	# изучить что надеть!
	# head, body, legs, shoes, accessories = str


	head = get_head(simple_weather)

	body = get_body(simple_weather)
	print(body)
	set_clothes = SetClothes(head=head, body=body, legs=head, shoes=head, accessories=head)

	return set_clothes


def get_head(simple_weather: SimpleWeather):
	heads = db_clothes.get_head_sql()

	# голова:
	if float(simple_weather.cur_weather) < 0:
		heads = [x for x in heads if int(x[4]) >= 2]
		head = random.choice(heads)

	if simple_weather.weather_description == "Ясно☀️" and float(simple_weather.cur_weather) > 13:
		heads = db_clothes.get_head_sql()
		heads = [x for x in heads if int(x[3]) == 'лето_солнце']
		head = random.choice(heads)

	el_head = ElClothes(name=head[1], img=head[-1])

	return el_head


def get_body(simple_weather: SimpleWeather):
	bodys = db_clothes.get_body_sql()
	_under_body = None
	under_body = ElClothes(name="", img="")
	outer_body = ElClothes(name="", img="")

	under_bodys = [x for x in bodys if not (x[3].startswith("верхнее") or x[3].startswith("нижнее"))]
	print("under_bodys ", under_bodys)

	if  0 < float(simple_weather.cur_weather) < 10:
		outer_bodys = [x for x in bodys if x[3].startswith("верхнее_осень")]
		_outer_body = random.choice(outer_bodys)
	if  float(simple_weather.cur_weather) < 0:
		outer_bodys = [x for x in bodys if x[3].startswith("верхнее_зима")]
		_outer_body = random.choice(outer_bodys)
		print('outer_bodys', outer_bodys)
	if  0 < float(simple_weather.cur_weather) < 10 and (simple_weather.weather_description == "Дождь🌦" or simple_weather.weather_description == "Гроза🌩" or simple_weather.weather_description == "Ливень🌧"):
		outer_bodys = [x for x in bodys if x[3].startswith("верхнее_дождь")]
		_outer_body = random.choice(outer_bodys)


	if float(simple_weather.cur_weather) > 20:
		under_bodys = [x for x in bodys if x[3].startswith("лето") or x[3].startswith("-")]
		under_bodys = [x for x in under_bodys if int(x[4]) == 1]
		_under_body = random.choice(under_bodys)

	if 15 <= float(simple_weather.cur_weather) < 20:
		under_bodys = [x for x in bodys if x[3].startswith("лето") or x[3].startswith("осень") or x[3].startswith("-")]
		under_bodys = [x for x in under_bodys if int(x[4]) <= 2]
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
		pass
		# надо подштаники

	if _outer_body:
		outer_body = ElClothes(name=_outer_body[1], img=_outer_body[-1])

	under_body = ElClothes(name=_under_body[1], img=_under_body[-1])

	el_body = ElBody(outerwear=outer_body, underwear=under_body)

	return el_body