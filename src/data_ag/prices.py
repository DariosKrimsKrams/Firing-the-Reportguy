import pandas as pd
from .utils.cache import cache_csv
from .utils.csv import download_csv


@cache_csv(cache_dir="./cache")
def download_prices(
    start_date: str = "2024-04-01",
    end_date: str = "2025-04-30",
    commodity_ids: list = None,
    market_ids: list = None,
    price_type_id: int = 15,
    time_aggregation: int = 1,
) -> pd.DataFrame:
    """
    Download prices from the WFP API.

    Parameters:
        start_date (str): Start date for the data in YYYY-MM-DD format.
        end_date (str): End date for the data in YYYY-MM-DD format.
        commodity_ids (list): List of commodity IDs to filter by.
        market_ids (list): List of market IDs to filter by.
        price_type_id (int): Price type ID to filter by. (I honwstly don't know what this is)
        time_aggregation (int): Time aggregation level. (same here...)

    Returns:
        pd.DataFrame: DataFrame containing the downloaded prices.
    """
    url = "https://api.vam.wfp.org/economicExplorer/Prices/PricesExport"

    return download_csv(
        url,
        json={
            "startDate": start_date,
            "endDate": end_date,
            "commodityID": commodity_ids,
            "marketID": market_ids,
            "priceTypeID": price_type_id,
            "timeAggregation": time_aggregation,
        },
    )
