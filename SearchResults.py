class SearchResults:
	def __init__(self, data):
		# {'set_name': 'Ra Yellow Mega Pack', 'set_code': 'RYMP-EN054', 'set_rarity': 'Common', 'set_rarity_code': '(C)', 'set_price': '1.39'}
		self.results = {}
		self.results["id"] = data['id']
		self.results["name"] = data['name']
		self.results["card_sets"] = {}

		for row in data['card_sets']:
			self.results["card_sets"][row['set_code']] = {}

			for key in row:
				if key == 'set_code':
					continue

				self.results["card_sets"][row['set_code']][key] = row[key]


		print(self.results)


	def get_card_set_param(self, card_set_id, param_value):
		if card_set_id not in self.results['card_sets']:
			return None
		return self.results['card_sets'][card_set_id][param_value]