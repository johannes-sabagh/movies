import statistics
import random
from movie_storage import movie_storage_sql as storage
import requests
from config import website_generator
import os
from dotenv import load_dotenv

load_dotenv()


def command_list_movies():
    """
    Display all movies with their year and rating.
    """

    # Retrieve all movies from storage
    all_movies = storage.list_movies()

    # Display total count
    print(f"{len(all_movies)} movies in total.")

    # Loop through and display each movie with its details
    for movie, data in all_movies.items():
        movie_year = data["year"]
        movie_rating = data["rating"]
        movie_poster = data["poster"]
        print(f"{movie} ({movie_year}) : {movie_rating}")


def fetch_movie(new_title):
    """
    Fetch movie details from the OMDb API by title.

    Args:
        new_title (str): The title of the movie to search for.

    Returns:
        tuple: A (title, year, imdb_rating) tuple if the movie is found.

    Raises:
        Exception: Prints any unexpected errors (e.g. network issues) to stdout.
    """
    api_key = os.environ.get("APIKEY")

    try:
        # Make a GET request to the OMDb API using the provided movie title
        movie_data = requests.get(f"https://www.omdbapi.com/?apikey={api_key}&t={new_title}")

        # OMDb returns this specific payload when no match is found
        if movie_data.json() == {'Response': 'False', 'Error': 'Movie not found!'}:
            return f"The movie {new_title} not found"

        # Extract the relevant fields from the JSON response
        new_title = movie_data.json()["Title"]
        new_year = movie_data.json()["Year"]
        new_rating = movie_data.json()["imdbRating"]
        new_poster = movie_data.json()["Poster"]
        return new_title, new_year, new_rating, new_poster

    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
        return None

    # to catch other errors

    except Exception as e:
        print(f"Error: {e}")


def add_movie():
    """
    Prompt the user for a movie title, fetch its details, and add it to the database.

    Validates that the user provides a non-empty title, then checks whether the
    movie already exists in storage before fetching from the OMDb API and saving.
    """

    # Keep prompting until the user enters a non-empty, non-whitespace title
    while True:
        try:
            new_title = input("Enter new movie name: ")
            if not new_title.strip():
                raise ValueError("invalid input")
            break
        except ValueError as e:
            print("invalid input")

    # Retrieve the current list of movies from storage to check for duplicates
    all_movies = storage.list_movies()

    # Only fetch and add the movie if it doesn't already exist in the database
    if not new_title in list(all_movies.keys()):
        try:
            # Fetch title, year, and IMDb rating from the OMDb API
            result = fetch_movie(new_title)

            # Handle the API failure explicitly before unpacking
            if result is None or isinstance(result, str):
                print(result or "Could not fetch movie data.")
                return

            new_title, new_year, new_rating, new_poster = result

            # Add the new movie entry to storage
            storage.add_movie(new_title, new_year, new_rating, new_poster)
        except Exception as e:
            print(f"The movie {new_title} is not found")

    else:
        print(f"Movie {new_title} already exist!")


def delete_movie():
    """
    Remove a movie from the database.
    """
    # Get the movie name to delete and not allowing empty input
    while True:
        try:
            movie_to_delete = input("Enter movie name to delete: ")
            if not movie_to_delete.strip():
                raise ValueError("invalid input")
            break
        except ValueError:
            print("invalid input")

    # Retrieve all movies from storage
    all_movies = storage.list_movies()

    # Check if movie exists before attempting deletion
    if movie_to_delete in list(all_movies.keys()):
        # Delete the movie from storage
        storage.delete_movie(movie_to_delete)
    else:
        # Inform user that movie doesn't exist
        print(f"Movie {movie_to_delete} doesn't exist!")


def update_movie():
    """
    Update the rating of an existing movie.
    """
    # Get the movie name to update and not allowing empty input
    while True:
        try:
            movie_to_update = input("Enter movie name: ")
            if not movie_to_update.strip():
                raise ValueError("invalid input")
            break
        except ValueError:
            print("invalid input")

    # Retrieve all movies from storage
    all_movies = storage.list_movies()

    # Check if movie exists before updating
    if movie_to_update in list(all_movies.keys()):
        # Get new rating from user and not allowing empty or wrong input
        while True:
            try:
                update_rating = float(input("Enter new movie rating (0-10): "))
                if update_rating > 10 or update_rating <0:
                    raise ValueError
                break
            except ValueError:
                print("must be a number between 0 an 10")

        # Update the movie rating in storage
        storage.update_movie(movie_to_update, update_rating)

    else:
        # Inform user that movie doesn't exist
        print(f"Movie {movie_to_update} doesn't exist!")


def stats():
    """
    Calculate and display statistics about movie ratings.
    """

    # Retrieve all movies from storage
    all_movies = storage.list_movies()
    if not all_movies:
        print("The movie database is empty!")
        return
    # Extract all ratings into a list
    ratings = []
    for movie, data in all_movies.items():
        ratings.append(data["rating"])

    if ratings:
        # Calculate statistical values
        average_rating = sum(ratings) / len(ratings)
        median_rating = statistics.median(ratings)
        max_value = max(ratings)
        min_value = min(ratings)
    else:
        print("no movies to show")

    # Find all movies with the highest rating
    max_rating = []
    for movie, data in all_movies.items():
        if data["rating"] == max_value:
            max_rating.append(movie)

    # Find all movies with the lowest rating
    min_rating = []
    for movie, data in all_movies.items():
        if data["rating"] == min_value:
            min_rating.append(movie)

    # Display all statistics
    print("Average rating:", "%.1f" % average_rating)
    print("Median rating:", "%.1f" % median_rating)
    print("Best movie(s):", end="")
    for movie in max_rating:
        print(f"  {movie}, {max_value}")

    print("Worst movie(s):", end="")
    for movie in min_rating:
        print(f"  {movie}, {min_value}")


def random_movie():
    """
    Suggest a random movie from the database.
    """

    # Retrieve all movies from storage
    all_movies = storage.list_movies()
    if not all_movies:
        print("The movie database is empty!")
        return
    # Select a random movie from all available movies
    movie_choice = random.choice(list(all_movies.keys()))

    # Display the randomly selected movie with its rating
    print(f"Your movie for tonight: {movie_choice}, it's rated {all_movies[movie_choice]["rating"]}")


def search_movie():
    """
    Search for movies by partial name match (case-insensitive).
    """
    # Get search text from user
    text_to_find = input("Enter part of movie name: ")

    # Retrieve all movies from storage
    all_movies = storage.list_movies()

    # Search through all movies for partial matches
    found = False
    for movie, data in all_movies.items():
        if text_to_find.casefold() in movie.casefold():
            print(movie + ",", data["rating"])
            found = True

    if not found:
        print("not found!")

def sort_movies_by_rating():
    """
    Display movies sorted by rating from highest to lowest.
    """

    # Retrieve all movies from storage
    all_movies = storage.list_movies()

    # Sort movies by rating in descending order
    for movie, data in sorted(all_movies.items(), key=lambda x: x[1]["rating"], reverse=True):
        print(f"{movie}: {data['rating']}")


def sort_movies_by_year():
    """
    Display movies sorted by year with user-specified order.
    """

    # Retrieve all movies from storage
    all_movies = storage.list_movies()

    # Ask user for sort order preference and accept only valid input y or n
    while True:
        sort_order = input("Do you want the latest movies first? (Y/N): ")
        if sort_order.casefold() == "Y".casefold() or sort_order.casefold() == "N".casefold():
            break
        print("invalid input")

    # Determine sort order based on user input
    if sort_order.casefold() == "y".casefold():
        order_answer = True  # Descending order (latest first)
    elif sort_order.casefold() == "N".casefold():
        order_answer = False  # Ascending order (oldest first)
    else:
        print("invalid answer")

    # Sort and display movies by year
    for movie, data in sorted(all_movies.items(), key=lambda x: x[1]["year"], reverse=order_answer):
        print(f"{movie}: {data['year']}")


def filter_movies():
    """
    Filter movies by minimum rating and year range.
    """

    # Retrieve all movies from storage
    all_movies = storage.list_movies()

    # Get filter criteria from user (default values if left blank)
    minimum_rating = int(input("Enter minimum rating (leave blank for no minimum rating): ") or 0)
    start_year = int(input("Enter start year (leave blank for no start year): ") or 0)
    end_year = int(input("Enter end year (leave blank for no end year): ") or 99999) # a high number for end year when no value is given

    # Filter movies based on criteria
    filtered_movies = {}
    for movie, data in all_movies.items():
        # Check if movie meets all filter criteria
        if minimum_rating <= data["rating"] and start_year <= data["year"] and end_year >= data["year"]:
            filtered_movies[movie] = {"year": data["year"], "rating": data["rating"]}

    # Display filtered results
    for movie, data in filtered_movies.items():
        movie_year = data["year"]
        movie_rating = data["rating"]
        print(f"{movie} ({movie_year}) : {movie_rating}")


def menu_display():
    """
    Display the main menu and handle user input.
    """

    while True:
        # Display menu options
        menu_text = "Menu:\n0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating\n9. Generate website\n"
        print(menu_text)

        # Get user's menu choice with error handling
        try:
            user_choice = int(input("Enter choice (1-10): "))
        except ValueError:
            # Handle non-integer input
            print("invalid choice")
            continue

        # Execute the corresponding function based on user choice
        if user_choice == 0:
            # Exit the program
            # Display goodbye message when exiting
            print("Bye!")
            return
        elif user_choice == 1:
            command_list_movies()
            wait_user = input("Press enter to continue")
        elif user_choice == 2:
            add_movie()
            wait_user = input("Press enter to continue")
        elif user_choice == 3:
            delete_movie()
            wait_user = input("Press enter to continue")
        elif user_choice == 4:
            update_movie()
            wait_user = input("Press enter to continue")
        elif user_choice == 5:
            stats()
            wait_user = input("Press enter to continue")
        elif user_choice == 6:
            random_movie()
            wait_user = input("Press enter to continue")
        elif user_choice == 7:
            search_movie()
            wait_user = input("Press enter to continue")
        elif user_choice == 8:
            sort_movies_by_rating()
            wait_user = input("Press enter to continue")
        elif user_choice == 9:
            TEXT_PLACEHOLDER = "__TEMPLATE_MOVIE_GRID__"
            TITLE_PLACEHOLDER = "__TEMPLATE_TITLE__"
            NEW_TITLE = "Johannes' Movie Collection"
            website_generator.create_final_html(TEXT_PLACEHOLDER, TITLE_PLACEHOLDER, NEW_TITLE)
            wait_user = input("Press enter to continue")
        else:
            # Handle invalid menu choices
            print("invalid choice")


def main():
    """
    Initialize and run the movie database application.
    """
    # Display welcome header
    print("********** My Movies Database **********")

    # Start the main menu loop


    menu_display()


# Entry point of the program
if __name__ == "__main__":
    main()