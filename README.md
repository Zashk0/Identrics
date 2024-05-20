
## Setup and Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/etl_news_project.git
    cd etl_news_project
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/Scripts/activate  # On Windows
    source venv/bin/activate      # On Linux/MacOS
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Install and configure ChromeDriver for Selenium**:

    ChromeDriver should be installed automatically using `webdriver_manager`, but ensure you have Google Chrome installed on your machine.

## Scraping Articles

1. **Run the CapitalBrief spider**:

    ```bash
    scrapy crawl capitalbrief_spider
    ```

   This will scrape articles from the CapitalBrief website and save them to `spiders/raw_data_capitalbrief.json`.

2. **Run the RestOfWorld spider**:

    ```bash
    scrapy crawl rest_of_world_spider
    ```

   This will scrape articles from the RestOfWorld website and save them to `spiders/raw_data_rest_of_world.json`.

## Database Setup

1. **Create the SQLite database and tables**:

    ```bash
    python -m api.main
    ```

   This command will also insert the scraped data into the database.

## Running the API

1. **Start the FastAPI server**:

    ```bash
    uvicorn api.main:app --reload
    ```

   The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

- **GET /articles/?page={n}**: Get all crawled articles and their properties paginated by 5 articles per page.
- **GET /articles/?date={date}**: Get list of articles from the specified date.
- **GET /articles/?author={author}**: Get list of articles by the specified author.
- **GET /article/{article_id}**: Get a single article by its ID.
- **POST /article/{article_id}**: Create a new article by sending JSON data in the request body.
- **DELETE /article/{article_id}**: Delete a single article by its ID.
- **PUT /article/{article_id}**: Update a single article by sending JSON data in the request body.
- **GET /articles/recent**: Retrieve the most recently published articles.
- **GET /articles/last**: Retrieve the last inserted article in the database.
- **GET /articles/search?q={query}**: Search articles by keywords in the title or body.
- **GET /articles/popular**: Fetch articles sorted by comment count.

## Additional Notes

- Ensure your system's Python environment is properly configured with all necessary dependencies.
- Adjust the Scrapy spiders and API settings as needed for different target websites or data structures.

## Contributing

Feel free to submit issues or pull requests if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License.
