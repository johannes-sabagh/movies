
import movie_storage_sql as storage


html_path = "_static/index_template.html"
def load_html_template(html_path):
    try:
        with open(html_path, "r") as html_template:
            return html_template.read()
    except FileNotFoundError:
        print(f"Error: Template file '{html_path}' not found.")
        raise
    except IOError as e:
        print(f"Error reading template file: {e}")
        raise

def create_html():
    try:
        all_movies = storage.list_movies()
    except Exception as e:
        print(f"Error fetching movies from storage: {e}")
        raise
    movie_list = []
    for movie, data in all_movies.items():
        movie_list.append(serialize_movie(movie, data))
    return ''.join(movie_list)


def serialize_movie(movie, data):
    try:
        year = data["year"]
        poster = data["poster"]
    except KeyError as e:
        print(f"Missing field {e} for movie '{movie}', skipping.")
        return ''

    parts = [
        '<li>',
        '<div class="movie">',
        f'<img class="movie-poster" src={poster} title=""/>',
        f'<div class="movie-title">{movie}</div>',
        f'<div class="movie-year">{year}</div>',
        '</div>',
        '</li>'
    ]
    return ''.join(parts)


def create_final_html(TEXT_PLACEHOLDER, TITLE_PLACEHOLDER, NEW_TITLE):
    try:
        old_html = load_html_template(html_path)
        new_html_text = create_html()
        final_html_text = old_html.replace(TEXT_PLACEHOLDER, new_html_text)
        final_html_text = final_html_text.replace(TITLE_PLACEHOLDER, NEW_TITLE)
        with open("_static/index.html", "w") as final_html:
            final_html.write(final_html_text)
        print("Website generated successfully!")
    except IOError as e:
        print(f"Error writing output HTML file: {e}")
        raise



