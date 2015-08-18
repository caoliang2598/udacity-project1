__author__ = 'caoliang'

import webbrowser
class Movie():
    def __init__(self, title, story_line, poster_image_url,
                 trailer_youtube_url):
        self.title = title
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url
        self.story_line = story_line