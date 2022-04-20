from objects import SaveManager as SM
from proccesing import ProcessData as PP
from scraper import ScrapeData as Scrape

Scrape()
movies, shows = SM().load_data()
SM().save_data(PP().sort_by_year(movies), 'Newest movies', False)
SM().save_data(PP().sort_by_rating(movies), 'Top rated movies', False)
SM().save_data(PP().top_10(movies), 'Top 10 movies', False)
SM().save_data(PP().newest_10(movies), 'Newest 10 movies', False)
SM().save_data(PP().avg_rating(movies, 2000, 2022), 'Avarage movie rating from 2000', False)
SM().save_data(PP().sort_by_year(shows), 'Newest shows', False)
SM().save_data(PP().sort_by_rating(shows), 'Top rated shows', False)
SM().save_data(PP().top_10(shows), 'Top 10 shows', False)
SM().save_data(PP().newest_10(shows), 'Newest 10 shows', False)
SM().save_data(PP().avg_rating(shows, 2000, 2022), 'Avarage show rating from 2000', True)
