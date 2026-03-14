import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import time

def search_images(query, count=200, api_key="YOUR_BING_API_KEY", max_retries=3, retry_delay=2):
    """
    Search images from Bing Image Search API.

    Args:
        query (str): Search term.
        count (int): Number of results to fetch (max depends on API limits).
        api_key (str): Your Bing API key.
        max_retries (int): Number of times to retry in case of failure.
        retry_delay (int): Seconds to wait between retries.

    Returns:
        list: List of image URLs.
    """
    endpoint = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": count}

    for attempt in range(max_retries):
        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses
            data = response.json()

            # Ensure 'value' exists in response
            if "value" not in data:
                print("Warning: 'value' key not found in API response.")
                return []

            # Extract image URLs
            return [img.get("contentUrl") for img in data["value"] if "contentUrl" in img]

        except (HTTPError, ConnectionError, Timeout) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
                return []
        except RequestException as e:
            print(f"Unexpected error: {e}")
            return []
        except ValueError:
            print("Error parsing JSON response.")
            return []

# Example usage:
if __name__ == "__main__":
    urls = search_images("puppies", count=10, api_key="YOUR_BING_API_KEY")
    print("Found URLs:", urls)
