import os
import json
import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Process, Queue


class ScrapeData(object):
    def __init__(self):
        shows_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'
        movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
        to_parse = self.parse_url(movies_url, shows_url)
        processes = []
        save_list = []
        queue = Queue()
        for item in to_parse:
            p = Process(target=self.parse_items, args=(item, queue,))
            p.start()
            processes.append(p)

        for process in processes:
            process.join()

        while queue.empty() is False:
            save_list.append(queue.get())

        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/data.json'
        with open(filename, 'w') as file:
            json.dump(save_list, file, indent=4)

    def parse_url(self, movies_url, shows_url):
        count = 0
        limit = 50
        parsed_list = []
        req = requests.get(movies_url)
        soup = BS(req.content, 'html.parser')
        titles = soup.findAll('td', class_='titleColumn')
        for item in titles:
            movie = {}
            if count < limit/2:
                movie['id'] = count
                movie['category'] = 'movie'
                movie['link'] = 'https://www.imdb.com' + item.a.get('href')
                parsed_list.append(movie)
                count += 1
        req = requests.get(shows_url)
        soup = BS(req.content, 'html.parser')
        titles = soup.findAll('td', class_='titleColumn')
        for item in titles:
            show = {}
            if count < limit:
                show['id'] = count
                show['category'] = 'show'
                show['link'] = 'https://www.imdb.com' + item.a.get('href')
                parsed_list.append(show)
                count += 1

        return parsed_list

    def parse_items(self, to_parse, queue):
        parsed_dict = {}
        print('Parsing: {}/50'.format(to_parse['id']+1))
        if to_parse['category'] == 'movie':
            parsed_dict['category'] = 'movie'
        else:
            parsed_dict['category'] = 'tv-show'
        req = requests.get(to_parse['link'])
        soup = BS(req.content, 'html.parser')
        data = soup.findAll('body')
        try:
            org_title = data[0].findAll(
                'div', {'data-testid': 'hero-title-block__original-title'})[0].text
            split = org_title.split()
            title = ''
            for item in split[2:]:
                title += item + ' '
            parsed_dict['title'] = title
        except IndexError:
            usual_title = data[0].findAll(
                'h1', {'data-testid': 'hero-title-block__title'})[0].text
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

        if parsed_dict['category'] == 'tv-show':
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

        queue.put(parsed_dict)