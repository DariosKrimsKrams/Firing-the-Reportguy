import io
import requests
import pandas as pd


def download_csv(*args, **kwargs):
    """
    Download CSV from a URL with optional pandas.read_csv kwargs.
    """
    headers = kwargs.pop("headers", None)
    if headers is None:
        # Default headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
    kwargs["headers"] = headers

    response = requests.post(*args, **kwargs)
    response.raise_for_status()
    # Read CSV content into DataFrame
    df = pd.read_csv(io.StringIO(response.text))
    return df
