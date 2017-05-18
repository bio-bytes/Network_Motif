import requests
from bs4 import BeautifulSoup


def get_years(query_url):
	r = requests.get(query_url)
	soup = BeautifulSoup(r.text, 'html.parser')
	indies = soup.find_all("div", class_="gs_ri")
	years = []
	for indie in indies:
		try:
			year = indie.find("div", class_="gs_a")
			year = year.find_all('a')[-1].next_sibling
			year = year.split(',')[1]
			year = year.split('-')[0].strip()
			assert(year.isdigit() and len(year) == 4) #make sure we scrape only year
			years.append(int(year))
		except:
			continue
	return years


def get_results(query, limit=100):
	start = 0
	years = {}
	while start <= limit - 10:
		query_url = "https://scholar.google.co.in/scholar?hl=en&q=" + query.replace(' ','+') + "&start=" + str(start)
		returned_years = get_years(query_url)
		for year in returned_years:
			if year in years:
				years[year] += 1
			else:
				years[year] = 1
		start += 10
	return years


if __name__ == "__main__":
	print get_results("network motifs", 20)
