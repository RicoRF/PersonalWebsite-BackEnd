# Backend API - FastAPI

This is the backend API for the project. It is built using [FastAPI](https://fastapi.tiangolo.com/) and provides endpoints for fetching LinkedIn and GitHub data.

## Requirements

Before running the backend, ensure you have the following installed:

- Python 3.10 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backend

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

   The server will start at `http://localhost:8000`.

2. Verify the server is running by visiting the automatically generated API docs:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## CORS Configuration

The backend is configured to allow requests from `http://localhost:3000` using FastAPI's `CORSMiddleware`. This is necessary for the frontend to make API requests to the backend.

## API Endpoints

### LinkedIn Data
- **URL:** `http://localhost:8000/linkedin`
- **Method:** `GET`
- **Description:** Fetches LinkedIn data.

### GitHub Data
- **URL:** `http://localhost:8000/github`
- **Method:** `GET`
- **Description:** Fetches GitHub data.

## Development Notes

- Update the `.env` file with any required environment variables.
- To add new endpoints, modify the `main.py` file.

## Troubleshooting

- If you encounter CORS issues, ensure the frontend is running on `http://localhost:3000` and matches the allowed origins in the backend.
- For missing dependencies, re-run `pip install -r requirements.txt`.

## License

This project is licensed under the [MIT License](LICENSE).
