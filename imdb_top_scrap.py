import requests
from bs4 import BeautifulSoup
import csv
import json

movie_list = []
top_movies_list = list()
top_movies_dict = {'imdb_top_250':{}}

def get_url_data():
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup

def extract_imdb_data(soup:object):
    global movie_list
    global top_movies_list
    t_body = soup.tbody
    t_rs = t_body.find_all('tr')

    for tr in t_rs:
        t_ds = tr.find_all('td')
        movie_datas = str(t_ds[1].get_text()).strip() + str(t_ds[2].get_text()).strip()
        movie_list.append(movie_datas)

    #print(movie_list)
    for movie in movie_list:
        number, name, date = movie.split('\n')
        top_movies_list.append([
            int(number[:-1]),
            name.strip(),
            date[1:5],
            date[-3:]
        ])


def convert_csv():
    
    header_list = ["NUMBER", "MOVIE NAME", "YEAR", "RATE"]
    rows = top_movies_list

    #name of csv file
    file_name = 'top_250_movies.csv'

    with open(file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header_list)
        for row in rows:
            csvwriter.writerow(row)

    
def convert_json():
    global top_movies_dict
    if top_movies_list:
        for movie in top_movies_list:
            top_movies_dict['imdb_top_250'].update({
                movie[0]:{
                    'movie_name':movie[1],
                    'date':movie[2],
                    'rate':movie[-1]
                }
            })
        top_movies_json = json.dumps(top_movies_dict, indent=4)
        with open('imdb_top_250.json', 'w', encoding='utf-8') as outfile:
            outfile.write(top_movies_json)
    else:
        return None


def main():
    soup = get_url_data()
    extract_imdb_data(soup)
    convert_csv()
    convert_json()


if __name__ == '__main__':
    main()
    