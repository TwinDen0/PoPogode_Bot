import Levenshtein

cites_coord = {
	"Москва": [55.45, 37.36],
	"Санкт-Петербург": [59.57, 30.19],
	"Владивосток": [43.07, 131.54],
	"Благовещенск": [50.27278, 127.54],
	"Казань": [55.47, 49.06],
	"Екатеринбург": [56.50, 60.36],
	"Новосибирск": [55.01, 82.55],
	"Омск": [54.59, 73.22],
	"Челябинск": [55.09, 61.24],
	"Уфа": [54.44, 55.59],
	"Самара": [53.12, 50.08],
	"Ростов-на-Дону": [47.14, 39.42],
	"Красноярск": [56.01, 92.50],
	"Пермь": [58.0, 56.19],
	"Воронеж": [51.40, 39.15],
	"Волгоград": [48.43, 44.30],
}

def get_city(city):

	find_city = ""
	best_ratio = 0

	for city_name in cites_coord:
		ratio = Levenshtein.ratio(city, city_name)
		if ratio > best_ratio:
			best_ratio = ratio
			find_city = city_name

	coord = cites_coord[find_city]

	return find_city, coord

