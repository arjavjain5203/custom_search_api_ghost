# Playwright Search API

A minimal Python-based automation service that uses Playwright to perform web searches and return raw HTML content via a FastAPI endpoint.

## Features

- **Automated Search**: Uses Playwright (Headless Chromium) to search on Google/DuckDuckGo.
- **Raw Content Extraction**: Returns the full HTML of the first organic search result.
- **API Endpoint**: Simple `POST /search` interface.
- **Container Ready**: Designed with headless mode in mind.

## Requirements

- Python 3.8+
- Playwright
- FastAPI
- Uvicorn

## Installation

1.  **Clone the repository** (or navigate to the project directory).
2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Install Playwright browsers**:
    ```bash
    playwright install chromium
    ```

## Usage

1.  **Start the API server**:
    ```bash
    uvicorn main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

2.  **Make a Search Request**:
    ```bash
    curl -X POST "http://127.0.0.1:8000/search" \
         -H "Content-Type: application/json" \
         -d '{"query": "What is FastAPI?"}'
    ```

3.  **Response**:
    ```json
    {
      "html_content": "<!DOCTYPE html><html>...</html>"
    }
    ```

## Project Structure

- `main.py`: FastAPI application and endpoint definition.
- `automation.py`: Core Playwright automation logic.
- `requirements.txt`: Python dependencies.
# custom_search_api_ghost
