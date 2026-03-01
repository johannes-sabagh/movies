import json
def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open("data.json", "r") as movies_data:
        all_movies = json.load(movies_data)
    return all_movies


def save_movies(all_movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open("data.json", "w") as movies_data:
        json.dump(all_movies, movies_data, indent=4)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    # Read existing data
    all_movies = get_movies()

    # Add new movie
    all_movies[title] = {"year":year, "rating":rating}

    # Write back to file
    save_movies(all_movies)




def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    # Read existing data
    all_movies = get_movies()

    del all_movies[title]

    # Write back to file
    save_movies(all_movies)


def update_movie(movie_to_update, update_rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    all_movies = get_movies()
    all_movies[movie_to_update]["rating"] = update_rating
    save_movies(all_movies)