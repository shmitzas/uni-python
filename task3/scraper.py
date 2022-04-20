# import time
import requests
from bs4 import BeautifulSoup as BS
# from multiprocessing import Process, Pool, freeze_support
# import threading

class ParseRequests(object):
    def __init__(self):
        shows_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'
        movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
        movies = self.parse_url(movies_url)
        # shows = self.parse_url

        print(len(movies))

        for item in movies:
            movie_data = self.parse_movie(item)
        # print('passed')
    def parse_url(self, url):
        count = 0
        parsed_list = []
        req = requests.get(url)
        soup = BS(req.content, 'html.parser')
        titles = soup.findAll('td', class_ = 'titleColumn')
        for item in titles:
            if count < 10:
                parsed_list.append('https://www.imdb.com'+item.a.get('href'))
                count += 1
        return parsed_list
    counter = 0
    def parse_movie(self, url):
        self.counter += 1
        parsed_dict = {}
        req = requests.get(url)
        soup = BS(req.content, 'html.parser')
        data = soup.findAll('body')
        print(url)
        org_title = data[0].findAll('div', {'data-testid':'hero-title-block__original-title'})[0].text
        usual_title = data[0].findAll('h1', {'data-testid':'hero-title-block__title'})[0].text
        if org_title != None:
            title_split = org_title.split()
            title = ''
            for item in title_split[2:]:
                title += item + ' '
            parsed_dict['title'] = title
        else:
            parsed_dict['title'] = usual_title      
        year = data[0].findAll(class_= 'sc-94726ce4-3 eSKKHi')[0].ul.li.a.text
        parsed_dict['year'] = year[0].text
        rating = soup.findAll(class_ = 'sc-7ab21ed2-1 jGRxWM')[0].text
        parsed_dict['rating'] = rating[0].text
        genre  = data[0].find_all('a', class_ = 'sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt')
        tmp_genre = []
        for item in genre:
            tmp_genre.append(item.text)
        parsed_dict['genre'] = tmp_genre
        return(parsed_dict)

ParseRequests()

