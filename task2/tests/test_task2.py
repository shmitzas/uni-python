import unittest
from task2 import ProcessData

class TestTask2(unittest.TestCase):
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

    test_dict1 = {
        'category': 'movie',
        'title': 'The Lord of the Rings: The Return of the King',
        'year': 2003,
        'rating': 8,
        'genre': ['action', 'drama', 'adventure']}
    test_dict2 = {
        'category': 'tv-show',
        'title': 'Chernobyl',
        'year': 2019,
        'rating': 9,
        'genre': ['history', 'thriller', 'drama'],
        'seasons': 1,
        'episodes': 5}
    test_movie = Movies(test_dict1['title'], test_dict1['year'], test_dict1['rating'], test_dict1['genre'])
    test_show = Shows(test_dict2['title'], test_dict2['year'], test_dict2['rating'], test_dict2['genre'], test_dict2['seasons'], test_dict2['episodes'])
    test_list = [test_movie, test_show]

    def test_avg_rating(self):      
        result = ProcessData.avg_rating(self, self.test_list, 2000, 2019)
        self.assertEqual(result, 8.5)
    
    def test_top_10(self):
        result = ProcessData.top_10(self, self.test_list)
        self.assertEqual(len(result), 2)

    def test_newest_10(self):
        result = ProcessData.newest_10(self, self.test_list)
        self.assertEqual(len(result), 2)
    
    def test_sort_by_rating(self):
        result = ProcessData.sort_by_rating(self, self.test_list)
        self.assertEqual(result[0].rating, 9)
    
    def test_sort_by_year(self):
        result = ProcessData.sort_by_year(self, self.test_list)
        self.assertEqual(result[0].year, 2019)
