# 🎬 Movies Database

A command-line application to manage a personal movie collection. Movies are fetched automatically from the OMDb API and stored in a local SQLite database. A static HTML website of your collection can also be generated.

## Features

- Add movies by title (auto-fetches year, rating, and poster from OMDb)
- Delete and update movies
- View stats (average, median, best, worst)
- Search, sort, and filter your collection
- Generate a static HTML website of your movie collection

## Project Structure

```
movies/
├── _static/
│   ├── index_template.html
│   ├── index.html          # generated output
│   └── style.css
├── config/
│   ├── website_generator.py
│   └── movie_storage_sql.py
├── main.py
└── requirements.txt
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```

## Usage

Use the numbered menu to navigate:

| Option | Action |
|--------|--------|
| 1 | List all movies |
| 2 | Add a movie |
| 3 | Delete a movie |
| 4 | Update a movie's rating |
| 5 | Show stats |
| 6 | Random movie suggestion |
| 7 | Search by title |
| 8 | Sort by rating |
| 9 | Generate HTML website |
| 0 | Exit |

## Dependencies

- `sqlalchemy` — database ORM for SQLite
- `requests` — HTTP calls to the OMDb API

## API

Movie data is fetched from [OMDb API](https://www.omdbapi.com/).
