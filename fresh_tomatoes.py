import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        #movie-carousel{
            margin-bottom: 60px;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // function to open trailer modal
        var open_trailer = function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        }
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', open_trailer);
        $(document).on('click', '.movie-carousel', open_trailer);
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-static-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>

    <div class="container">
        <div class="page-header">
            <h1>Featured Movies</h1>
        </div>
        <div id="movie-carousel" class="carousel slide" data-ride="carousel">
            <!-- Indicators -->
            <ol class="carousel-indicators">
                {movie_sliders_indicators}
            </ol>

            <!-- Wrapper for slides -->
            <div class="carousel-inner" role="listbox">
                {movie_sliders}
            </div>

            <!-- Left and right controls -->
            <a class="left carousel-control" href="#movie-carousel" role="button" data-slide="prev">
                <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
                <span class="sr-only">Previous</span>
            </a>
            <a class="right carousel-control" href="#movie-carousel" role="button" data-slide="next">
                <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
                <span class="sr-only">Next</span>
            </a>
        </div>
    </div>

    <div class="container">
      {movie_tiles}
    </div>

  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''
# Movie carousel html template
movie_slider_content = '''
<div class={content_class!r}>
    <a href="#" class="movie-carousel" data-trailer-youtube-id={data_trailer_youtube_id} data-toggle="modal" data-target="#trailer">
        <img src="{poster_image_url}" alt="Flower" class="img-responsive center-block">
        <div class="carousel-caption">
            <h3>{movie_slider_title}</h3>
            <p>{movie_slider_description}</p>
        </div>
    </a>
</div>
'''

# Movie carousel indicator html template
movie_slider_indicator_content = '''
<li data-target="#movie-carousel" data-slide-to={slide_to_index:d} class={indicator_class!r}></li>
'''


def create_movie_slider_indicator(movies):
    indicators = ''

    # .active class needs to be set for first element
    indicators += movie_slider_indicator_content.format(
        slide_to_index=0,
        indicator_class="active")

    # Make indicators
    index = 1
    for movie in movies[1:]:
        indicators += movie_slider_indicator_content.format(
            slide_to_index=index,
            indicator_class="")
        index += 1

    return indicators


def create_movie_slider_content(movies):
    contents = ''

    # .active class needs to be set for first element
    contents += movie_slider_content.format(
        poster_image_url=movies[0].poster_image_url,
        content_class="item active",
        movie_slider_title=movies[0].title,
        movie_slider_description="",
        data_trailer_youtube_id=extract_youtube_id(movies[0]))

    # Append slides which will be used inside carousel
    for movie in movies[1:]:
        contents += movie_slider_content.format(
            poster_image_url=movie.poster_image_url, content_class="item",
            movie_slider_title=movie.title,
            movie_slider_description="",
            data_trailer_youtube_id=extract_youtube_id(movie))
    return contents


# Extract Youtube Trailer ID
def extract_youtube_id(movie):
    youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
    youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+',
                                                     movie.trailer_youtube_url)
    trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None
    return trailer_youtube_id


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        trailer_youtube_id = extract_youtube_id(movie)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the placeholder for the movie tiles with the actual dynamically generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies),
        movie_sliders=create_movie_slider_content(movies),
        movie_sliders_indicators=create_movie_slider_indicator(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)  # open in a new tab, if possible