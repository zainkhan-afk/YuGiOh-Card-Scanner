import requests
from SearchResults import SearchResults

class InfoScraper:
	def __init__(self):
		# Example URL "https://db.ygoprodeck.com/api/v7/cardinfo.php?name=CRYSTAL%20RELEASE"
		self.base_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name="


	def search_database(self, card_name):
		url = self.base_url + card_name
		response = requests.post(url)
		data = response.json()
		if "error" in data:
			return None

		# print(data)
		# for i, row in enumerate(data['data'][0]['card_sets']):
		# 	print(i, row)

		# return data['data'][0]
		return SearchResults(data['data'][0])


if __name__ == "__main__":
	IS = InfoScraper()
	IS.search_database("Gachi Gachi Gantetsu")