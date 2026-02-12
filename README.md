# Custom Search API (Ghost)

A minimal, Playwright-based Search API that automates DuckDuckGo searches and returns raw HTML content.

## Features

- **FastAPI Backend**: Simple `POST /search` endpoint.
- **Playwright Automation**: Uses a real browser instance (Chromium) to bypass basic bot detection.
- **DuckDuckGo Only**: Configured to search DuckDuckGo (HTML Lite version) for reliability and speed.
- **Bot Mitigation**: Includes User-Agent spoofing and realistic interaction delays.
- **Headful Mode**: Browser window is visible for debugging purposes (can be disabled in code).

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/arjavjain5203/custom_search_api_ghost.git
    cd custom_search_api_ghost
    ```

2.  **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

## Usage

1.  **Start the Server**
    ```bash
    uvicorn main:app --port 8000
    ```

2.  **Make a Search Request**
    ```bash
    curl -X POST "http://127.0.0.1:8000/search" \
         -H "Content-Type: application/json" \
         -d '{"query": "Who is the PM of India?"}'
    ```

## API Endpoint

### `POST /search`

-   **Request Body**:
    ```json
    {
      "query": "string"
    }
    ```
-   **Response**: Returns the raw HTML content of the first search result page.
    ```json
    {
      "html_content": "<!DOCTYPE html>..."
    }
    ```
