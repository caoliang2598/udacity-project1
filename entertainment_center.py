__author__ = 'caoliang'

from media import Movie
from fresh_tomatoes import open_movies_page

mad_max = Movie("Mad Max: Fury Road",
                "In a stark desert landscape where humanity is broken, two rebels just might be able to restore order: Max, a man of action and of few words, and Furiosa, a woman of action who is looking to make it back to her childhood homeland.",
                "http://ia.media-imdb.com/images/M/MV5BMTUyMTE0ODcxNF5BMl5BanBnXkFtZTgwODE4NDQzNTE@._V1_SY317_CR2,0,214,317_AL_.jpg",
                "https://www.youtube.com/watch?v=hEJnMQG9ev8")

san_andreas = Movie("San Andreas",
                    "In the aftermath of a massive earthquake in California, a rescue-chopper pilot makes a dangerous journey across the state in order to rescue his daughter.",
                    "http://ia.media-imdb.com/images/M/MV5BNjI4MTgyOTAxOV5BMl5BanBnXkFtZTgwMjQwOTA4NTE@._V1_SX214_AL_.jpg",
                    "https://www.youtube.com/watch?v=23VflsU3kZE")

avengers_age_of_ultron = Movie("Avengers: Age of Ultron",
                               "When Tony Stark and Bruce Banner try to jump-start a dormant peacekeeping program called Ultron, things go horribly wrong and it's up to Earth's Mightiest Heroes to stop the villainous Ultron from enacting his terrible plans.",
                               "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                               "https://www.youtube.com/watch?v=tmeOjFno6Do")

ted_second = Movie("Ted 2",
                  "Newlywed couple Ted and Tami-Lynn want to have a baby, but in order to qualify to be a parent, Ted will have to prove he's a person in a court of law.",
                  "http://ia.media-imdb.com/images/M/MV5BMjEwMDg3MDk1NF5BMl5BanBnXkFtZTgwNjYyODA1NTE@._V1_SX214_AL_.jpg",
                  "https://www.youtube.com/watch?v=S3AVcCggRnU")


def get_movie_db():
    return [mad_max, san_andreas, avengers_age_of_ultron, ted_second]

if __name__ == "__main__":
    open_movies_page(get_movie_db())
    pass