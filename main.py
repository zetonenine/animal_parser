import requests
from bs4 import BeautifulSoup
from sqliter import SQLighter
import time

db = SQLighter('tables.db')
start_time = time.time()

db.create()


def parse():

	web = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
	headers = {'YOUR-OWN'}

	full_page = requests.get(web, headers=headers)
	soup = BeautifulSoup(full_page.content, 'html.parser')
	div = soup.find_all('div', attrs={'id': 'mw-pages'})

	result = {}

	while web:
		full_page = requests.get(web, headers=headers)
		soup = BeautifulSoup(full_page.content, 'html.parser')
		div = soup.find_all('div', attrs={'id': 'mw-pages'})

		pack = []

		for i in div:
			divList = i.findAll('div', attrs={'class': 'mw-content-ltr'})

			for j in divList:
				divList2 = j.findAll('div', attrs={'class': 'mw-category'})

				for q in divList2:
					divList3 = q.select('div', attrs={'class': 'mw-category-group'})
					divList3 = list(divList3)
					pack.append(divList3)
					pack = pack[0]

					for s in divList3:
						letter = s.select('h3', text=True)
						word = s.select('li', text=True)
						letter = list(letter[0])[0]

						if letter == 'A':
							break

						if letter not in result.keys():
							result[letter] = 0

						for each in word:
							result[letter] += 1
							db.add_animal(letter, each.text)

					print(result)

		if letter != 'A':
			for li in div:
				link = li.find('a', href=True, text='Следующая страница')
				web = 'https://ru.wikipedia.org' + link['href']
				print(web)
		else:
			web = None

	print('\nВышел из цикла while')
	return result


result = parse()

print("\n--- %s seconds ---" % (time.time() - start_time))