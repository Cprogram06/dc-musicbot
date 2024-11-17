import requests  # Library for making HTTP requests


def get_playlist_items(api_key: str, playlist_id: str, max_items: int = 25) -> list:
    """
    Fetches video titles from a YouTube playlist using the YouTube Data API.

    Args:
        api_key (str): The API key for accessing the YouTube Data API.
        playlist_id (str): The unique ID of the YouTube playlist.
        max_items (int): The maximum number of video titles to retrieve. Defaults to 25.

    Returns:
        list: A list of video titles from the playlist.
    """
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        'part': 'snippet',
        'playlistId': playlist_id,
        'key': api_key,
        'maxResults': 50  # API maximum limit per request
    }

    items_retrieved = 0  # Counter for retrieved items
    results = []  # List to store video titles

    while url and items_retrieved < max_items:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Ensure proper HTTP response
        data = response.json()

        # Process the results
        for item in data.get('items', []):
            if items_retrieved < max_items:
                results.append(item['snippet']['title'])
                items_retrieved += 1
            else:
                break

        # Check for next page token
        next_page_token = data.get('nextPageToken')
        if next_page_token and items_retrieved < max_items:
            params['pageToken'] = next_page_token
        else:
            break

    return results
