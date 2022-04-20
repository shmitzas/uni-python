import os
import json
import requests
from bs4 import BeautifulSoup as BS


class ScrapeData(object):
    def __init__(self):
        shows_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'
        movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
        movies_links = self.parse_url(movies_url)
        shows_links = self.parse_url(shows_url)
        to_parse = len(movies_links + shows_links)
        counter = 0
        save_list = []
        for item in movies_links:
            save_list.append(self.parse_item(item))
            counter += 1
            print('Parsed {} / {}'.format(counter, to_parse))
        for item in shows_links:
            save_list.append(self.parse_item(item, True))
            counter += 1
            print('Parsed {} / {}'.format(counter, to_parse))

        filename = os.path.dirname(__file__) + '/data.json'
        with open(filename, 'w') as file:
            json.dump(save_list, file, indent=4)

    def parse_url(self, url):
        count = 0
        parsed_list = []
        req = requests.get(url)
        soup = BS(req.content, 'html.parser')
        titles = soup.findAll('td', class_='titleColumn')
        for item in titles:
            if count < 50:
                parsed_list.append('https://www.imdb.com' + item.a.get('href'))
                count += 1
        return parsed_list

    def parse_item(self, url, show=False):
        parsed_dict = {}
        if show == True:
            parsed_dict['category'] = 'tv-show'
        else:
            parsed_dict['category'] = 'movie'

        req = requests.get(url)
        soup = BS(req.content, 'html.parser')
        data = soup.findAll('body')

        org_title = data[0].findAll(
            'div', {'data-testid': 'hero-title-block__original-title'})[0].text
        usual_title = data[0].findAll(
            'h1', {'data-testid': 'hero-title-block__title'})[0].text
        if org_title != None:
            split = org_title.split()
            title = ''
            for item in split[2:]:
                title += item + ' '
            parsed_dict['title'] = title
        else:
            parsed_dict['title'] = usual_title
        year = data[0].findAll(class_='sc-94726ce4-3 eSKKHi')[0].ul.a.text
        if '\u2013' in year:
            split = year.split('\u2013')
            parsed_dict['year'] = int(split[0])
        else:
            parsed_dict['year'] = int(year)
        rating = soup.findAll(
            class_='sc-7ab21ed2-1 jGRxWM')[0].text
        parsed_dict['rating'] = float(rating)
        genre = data[0].find_all(
            'a', class_='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt')
        tmp_genre = []
        for item in genre:
            tmp_genre.append(item.text)
        parsed_dict['genre'] = tmp_genre

        if show == True:
            browse = data[0].findAll(
                class_='sc-93b8eec8-4 dDCqHi')[0]  # seasons div
            try:
                seasons = browse.findAll(
                    class_='ipc-button__text')[1].text  # single season
                split = seasons.split()
                parsed_dict['seasons'] = int(split[0])
            except IndexError:
                seasons = browse.findAll(
                    'label', {'for': 'browse-episodes-season'})[0].text  # multiple seasons
                split = seasons.split()
                parsed_dict['seasons'] = int(split[0])

            episodes = data[0].findAll(
                'div', {'data-testid': 'episodes-header'})[0].h3.span.text
            parsed_dict['episodes'] = int(episodes)
            return(parsed_dict)
        else:
            return(parsed_dict)
