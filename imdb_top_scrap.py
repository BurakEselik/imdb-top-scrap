import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

result = requests.get(url)
soup = BeautifulSoup(result.text, 'html.parser')

t_body = soup.tbody

t_rs = t_body.find_all('tr')
movie_list = []
top_movies_list = list()
for tr in t_rs:
    t_ds = tr.find_all('td')
    movie_datas = str(t_ds[1].get_text()).strip() + str(t_ds[2].get_text()).strip()
    movie_list.append(movie_datas)

#print(movie_list)
for movie in movie_list:
    number, name, date = movie.split('\n')
    top_movies_list.append([
        name.strip(),
        date[1:5],
        date[-3:]
    ])

print(top_movies_list)