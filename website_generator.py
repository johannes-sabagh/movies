
import movie_storage_sql as storage


html_path = "_static/index_template.html"


def load_html_template(html_path):
    """
    Load and return the contents of an HTML template file.

    Args:
        html_path (str): Path to the HTML template file.

    Returns:
        str: The full contents of the template file.

    Raises:
        FileNotFoundError: If the template file does not exist at the given path.
        IOError: If the file cannot be read due to a system error.
    """
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
    """
    Build an HTML string of all movies retrieved from storage.

    Fetches all movies from the storage layer and serializes each one
    into an HTML list item using serialize_movie().
    """

    try:
        all_movies = storage.list_movies()
    except Exception as e:
        print(f"Error fetching movies from storage: {e}")
        raise
    movie_list = []
    for movie, data in all_movies.items():
        # Serialize each movie and collect the resulting HTML snippets
        movie_list.append(serialize_movie(movie, data))
    return ''.join(movie_list)


def serialize_movie(movie, data):
    """
    Serialize a single movie entry into an HTML list item string.
    """

    try:
        year = data["year"]
        poster = data["poster"]
    except KeyError as e:
        # Skip movies with incomplete data rather than halting the whole render
        print(f"Missing field {e} for movie '{movie}', skipping.")
        return ''

    # Build the HTML structure for a single movie card
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
    """
    Generate the final HTML page by injecting movie data into the template.

    Loads the HTML template, replaces the movie list placeholder with
    generated movie HTML, swaps the title placeholder with a new title,
    and writes the result to '_static/index.html'.

    Args:
        TEXT_PLACEHOLDER (str): The placeholder string in the template
                                 to be replaced with the movie list HTML.
        TITLE_PLACEHOLDER (str): The placeholder string in the template
                                  to be replaced with the new page title.
        NEW_TITLE (str): The title to insert into the HTML page.

    Raises:
       IOError: If the output file cannot be written.
    """
    try:
        # Load the base template and generate the dynamic movie content
        old_html = load_html_template(html_path)
        new_html_text = create_html()

        # Inject the movie list and page title into the template
        final_html_text = old_html.replace(TEXT_PLACEHOLDER, new_html_text)
        final_html_text = final_html_text.replace(TITLE_PLACEHOLDER, NEW_TITLE)

        # Write the completed HTML to the output file
        with open("_static/index.html", "w") as final_html:
            final_html.write(final_html_text)
        print("Website generated successfully!")
    except IOError as e:
        print(f"Error writing output HTML file: {e}")
        raise