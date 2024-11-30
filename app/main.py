from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import httpx
from datetime import date
import json
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Scrapin API key and URL
SCRAPIN_KEY = os.getenv("SCRAPIN_API_KEY")
SCRAPIN_URL = "https://api.scrapin.io/enrichment/profile"

# Cache file path
CACHE_FILE = "linkedin_cache.json"

@app.get("/linkedin")
async def get_profile(linkedInUrl: str = "https://www.linkedin.com/in/ferranterico/"):
    # Validate Scrapin API key
    if not SCRAPIN_KEY:
        raise HTTPException(status_code=500, detail="Scrapin API key is missing")

    # Get today's date
    today = date.today()

    try:
        # Ensure the cache file exists
        if not os.path.exists(CACHE_FILE):
            # Initialize the cache file with default content
            with open(CACHE_FILE, "w") as cache_file:
                json.dump({"last_request_date": None, "data": None}, cache_file)

        # Load the cache content
        with open(CACHE_FILE, "r") as cache_file:
            cache = json.load(cache_file)

        # If the cache is for today, return the cached data
        if cache["last_request_date"] == str(today):
            return {"message": "Cached data", "data": cache["data"]}

        # If it's an even day, use the cache if available or make a request
        if today.day % 2 == 0:
            if cache["data"]:
                return {"message": "Cached data (even day)", "data": cache["data"]}
            else:
                return await make_scrapin_request(linkedInUrl, today)

        # If it's an uneven day, make a new request
        return await make_scrapin_request(linkedInUrl, today)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(exc)}"
        )


async def make_scrapin_request(linkedInUrl, today):
    """Make a request to the Scrapin API and update the cache."""
    query_params = {"apikey": SCRAPIN_KEY, "linkedInUrl": linkedInUrl}

    try:
        # Make an async request to the Scrapin API
        async with httpx.AsyncClient() as client:
            response = await client.get(SCRAPIN_URL, params=query_params)

        # Handle non-200 responses
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Scrapin API: {response.json()}"
            )

        # Save the response to the cache
        new_cache = {
            "last_request_date": str(today),
            "data": response.json()
        }
        with open(CACHE_FILE, "w") as cache_file:
            json.dump(new_cache, cache_file)

        # Return the API response
        return {"message": "Fresh data from Scrapin API", "data": response.json()}

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while requesting the Scrapin API: {str(exc)}"
        )


@app.get("/github")
async def get_user_repos():
    """Fetch public repositories for the user 'ricorf'."""
    url = "https://api.github.com/users/ricorf/repos"  # GitHub API URL for 'ricorf'

    try:
        # Make an async request to the GitHub API
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        # Handle non-200 responses
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"GitHub API error: {response.json()}"
            )

        # Return the response JSON
        return response.json()

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while requesting the GitHub API: {str(exc)}"
        )
