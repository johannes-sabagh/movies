
import movie_storage_sql as storage


html_path = "_static/index_template.html"
def load_html_template(html_path):
    with open(html_path, "r") as html_template:
        return html_template.read()

def create_html():
    all_movies = storage.list_movies()
    new_html = ''
    for movie, data in all_movies.items():
        new_html += serialize_movie(movie, data)
    return new_html


def serialize_movie(movie, data):
    new_html = ''
    title = movie
    year = data["year"]
    poster = data["poster"]
    new_html += f'<li><div class="movie"><img class="movie-poster" src={poster} title=""/><div class="movie-title">{title}</div><div class="movie-year">{year}</div></div></li><li>'
    return new_html


def create_final_html(TEXT_PLACEHOLDER, TITLE_PLACEHOLDER, NEW_TITLE):
    old_html = load_html_template(html_path)
    new_html_text = create_html()
    final_html_text = old_html.replace(TEXT_PLACEHOLDER, new_html_text)
    final_html_text = final_html_text.replace(TITLE_PLACEHOLDER, NEW_TITLE)
    with open("_static/index.html", "w") as final_html:
        final_html.write(final_html_text)


#print(all_movies)
#print(create_html(all_movies))
#create_final_html(TEXT_PLACEHOLDER, TITLE_PLACEHOLDER, NEW_TITLE)
