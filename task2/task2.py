import json
import os

class Movies(object):
    def __init__(self, title, year, rating, genre):
        self.title = title
        self.year = year
        self.rating = rating
        self.genre = genre

class Shows(object):
    def __init__(self, title, year, rating, genre, seasons, episodes):
        self.title = title
        self.year = year
        self.rating = rating
        self.genre = genre
        self.seasons = seasons
        self.episodes = episodes

class ProcessData(object):
    def sort_by_year(self, data):
        sorted_data = sorted(
            data, key=lambda d: d.year, reverse=True)
        return sorted_data

    def sort_by_rating(self, data):
        sorted_data = sorted(
            data, key=lambda d: d.rating, reverse=True)
        return sorted_data

    def top_10(self, data):
        top_n_list = []
        data = ProcessData.sort_by_rating(self, data)
        for i in range(len(data)):
            if i < 10:
                top_n_list.append(data[i])
        return top_n_list

    def newest_10(self, data):
        top_n_list = []
        data = ProcessData.sort_by_year(self, data)
        for i in range(len(data)):
            if i < 10:
                top_n_list.append(data[i])
        return top_n_list

    def avg_rating(self, data, start_y, end_y):
        avg = 0
        count = 0
        for i in range(len(data)):
            if start_y <= end_y:
                if data[i].year <= end_y and data[i].year >= start_y:
                    avg += data[i].rating
                    count += 1
            else:
                if data[i].year >= end_y and data[i].year <= start_y:
                    avg += data[i].rating
                    count += 1
        avg = avg / count
        return round(avg, 2)

class SaveManager(object):
    def load_data(self):
        movies = []
        tv_shows = []
        filename = os.path.dirname(__file__) + '/' + 'data.json'
        try:
            if os.stat(filename).st_size > 0:
                with open(filename, encoding="utf-8") as file:
                    from_json = json.load(file)
                    for item in from_json:
                        if item['category'] == 'movie':
                            movie = Movies(item['title'], item['year'], item['rating'], item['genre'])
                            movies.append(movie)
                        elif item['category'] == 'tv-show':
                            show = Shows(item['title'], item['year'], item['rating'], item['genre'], item['seasons'], item['episodes'])
                            tv_shows.append(show)
                        else:
                            print("Some item is neither a movie, nor a tv show!")
                return movies, tv_shows
            else:
                print('File "data.json" is empty!')
                exit()
        except OSError:
            print('File "data.json" does not exist!')
            exit()
        except KeyError:
            print('Some item in "data.json" is empty or missing an attribute!')
            exit()

    
    save_dict = {}
    def save_data(self, data, data_name, write):
        filename = os.path.dirname(__file__) + '/output.json'
        output_data = []
        test_float = 1.2
        if type(data) is not type(test_float):
            for item in data:
                output_data.append(item.__dict__)
                self.save_dict[data_name] = output_data
        else:
            self.save_dict[data_name] = data
        if write == True:
            with open(filename, 'w') as file:
                json.dump(self.save_dict, file, indent=4)

# OUTSIDE ALL CLASSES

sm = SaveManager()

movies, shows = sm.load_data()
data = ProcessData()
sm.save_data(data.sort_by_year(movies), 'Newest movies', False)
sm.save_data(data.sort_by_rating(movies), 'Top rated movies', False)
sm.save_data(data.top_10(movies), 'Top 10 movies', False)
sm.save_data(data.newest_10(movies), 'Newest 10 movies', False)
sm.save_data(data.avg_rating(movies, 2000, 2022), 'Avarage movie rating from 2000', False)

sm.save_data(data.sort_by_year(shows), 'Newest shows', False)
sm.save_data(data.sort_by_rating(shows), 'Top rated shows', False)
sm.save_data(data.top_10(shows), 'Top 10 shows', False)
sm.save_data(data.newest_10(shows), 'Newest 10 shows', False)
sm.save_data(data.avg_rating(shows, 2000, 2022), 'Avarage show rating from 2000', True)