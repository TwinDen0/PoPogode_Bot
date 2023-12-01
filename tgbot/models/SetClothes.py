from dataclasses import dataclass


@dataclass
class ElClothes:
	name: str
	img: str

@dataclass
class ElBody:
	outerwear: ElClothes
	underwear: ElClothes


@dataclass
class SetClothes:
	head: ElClothes
	body: ElBody
	legs: ElClothes
	shoes: ElClothes
	accessories: ElClothes
