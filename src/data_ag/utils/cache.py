import os
import json
import hashlib
import pandas as pd
from functools import wraps


def cache_csv(cache_dir="csv_cache"):
    """
    Decorator to cache the result of CSV-downloading functions.

    The decorated function should return a pandas.DataFrame.
    Caches the DataFrame to a CSV file named based on a hash of args/kwargs.

    Parameters:
        cache_dir (str): Directory where cached CSVs are stored.
    """
    # Ensure cache directory exists
    os.makedirs(cache_dir, exist_ok=True)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique key from function name + args + kwargs
            key_data = {"func": func.__name__, "args": args, "kwargs": kwargs}
            # Serialize key data to string
            key_str = json.dumps(key_data, sort_keys=True, default=str)
            # Create a hash of the key
            key_hash = hashlib.md5(key_str.encode("utf-8")).hexdigest()
            # Build cache filename
            cache_filename = f"{func.__name__}_{key_hash}.csv"
            cache_path = os.path.join(cache_dir, cache_filename)

            # If cache exists, load and return
            if os.path.exists(cache_path):
                print(f"Loading cached CSV from {cache_path}")
                return pd.read_csv(cache_path)

            # Otherwise, call the function and cache its result
            df = func(*args, **kwargs)
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Cached function must return a pandas DataFrame")
            df.to_csv(cache_path, index=False)
            print(f"Cached CSV saved to {cache_path}")
            return df

        return wrapper

    return decorator


# Usage Example
if __name__ == "__main__":

    @cache_csv(cache_dir="my_data_cache")
    def download_data(source_url: str, **options) -> pd.DataFrame:
        """Download CSV from a URL with optional pandas.read_csv kwargs."""
        return pd.read_csv(source_url, **options)

    # First call downloads and caches
    df1 = download_data("https://example.com/data.csv", sep=";")

    # Second call with same arguments uses cache
    df2 = download_data("https://example.com/data.csv", sep=";")
