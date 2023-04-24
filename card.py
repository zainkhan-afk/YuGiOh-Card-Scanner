class Card:
	def __init__(self, ID, card_set, name, rarity, language, condition):
		self.ID = ID
		self.card_set = card_set
		self.name = name
		self.rarity = rarity
		self.language = language
		self.condition = condition


	def __str__(self):
		data = f'''
Card ID: {self.ID}
Card Name: {self.name}
Card Set: {self.card_set}
Card Rarity: {self.rarity}
Language: {self.language}
Condition: {self.condition}
		'''
		return data


if __name__ == "__main__":
	c = Card(1, 'ABC-EN000', 'Test Card', 'Rare', 'EN', 'New')
	# print(c)
	str(c)