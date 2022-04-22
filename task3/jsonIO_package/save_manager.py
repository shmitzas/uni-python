import os
import json
from task2_package.movies import *
from task2_package.shows import *

class SaveManager(object):
    def load_data(self):
        movies = []
        tv_shows = []
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/data.json'
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
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/output.json'
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