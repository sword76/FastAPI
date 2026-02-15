# FastAPI Hotel Management API

This project implements a simple Hotel Management API using FastAPI, providing basic CRUD-like operations for hotel records. It demonstrates the use of FastAPI for building robust and high-performance web APIs in Python.

## Features

*   **Retrieve Hotels**: Fetch a list of all hotels or a specific hotel by ID or title.
*   **Update Hotel**: Completely replace a hotel record.
*   **Partially Update Hotel**: Modify specific fields of an existing hotel record.
*   **Synchronous/Asynchronous Endpoints**: Examples of both synchronous and asynchronous API endpoints.

## Technologies Used

*   **Python**: The core programming language.
*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Pydantic**: Used for data validation and settings management, integrated seamlessly with FastAPI.
*   **Uvicorn**: An ASGI server, used to run the FastAPI application.

## Setup

Follow these steps to get the project up and running on your local machine.

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/your-username/FastAPI-Hotel-API.git
    cd FastAPI-Hotel-API
    ```
    (Note: Replace `your-username` and `FastAPI-Hotel-API` with actual values if this project is hosted on GitHub.)

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To start the FastAPI application using Uvicorn:

### Development Mode (with hot-reloading)

```bash
uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

### Production Mode

```bash
uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 3
```

The API will be accessible at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## API Endpoints

The primary endpoints are defined in `src/api/hotels.py`.

*   **GET `/hotels`**: Retrieve a list of all hotels or filter by `id`, `title`, and paginate using `page` and `per_page`.
*   **GET `/hotels/sync/{id}`**: Example of a synchronous endpoint.
*   **GET `/hotels/async/{id}`**: Example of an asynchronous endpoint.
*   **PUT `/hotels/{hotel_id}`**: Fully update a hotel record.
*   **PATCH `/hotels/{hotel_id}`**: Partially update a hotel record.

## Project Structure

```
.
├── src/
│   ├── main.py             # Main FastAPI application entry point
│   ├── api/
│   │   ├── dependencies.py # API dependencies (currently empty)
│   │   └── hotels.py       # Hotel-related API endpoints and logic
│   └── schemas/
│       └── hotels.py       # Pydantic models for data validation (currently empty but can be extended)
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── GEMINI.md             # Gemini-specific project overview
└── ... (other files like .gitignore, venv/, etc.)
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any features, bug fixes, or improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. (Note: A LICENSE file would need to be created.)
