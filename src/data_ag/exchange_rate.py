import pandas as pd

from .utils.cache import cache_csv
from .utils.csv import download_csv


@cache_csv(cache_dir="./cache")
def download_exchange_rates(
    adm0_code: int = 238,  # country code?
    rate_type: str = "Official",  # Parralel
) -> pd.DataFrame:
    url = "https://api.vam.wfp.org/economicExplorer/Currency/ExchangeRateExport"
    data = {
        "adm0Code": adm0_code,
        "rateType": rate_type,
    }

    return download_csv(
        url,
        json=data,
    )


def get_exchange_rate(
    start_date: str,
    end_date: str,
    adm0_code: int = 238,  # country code?
    rate_type: str = "Official",  # Parralel
):
    """
    Dates in YYYY-MM-DD format
    """
    df = download_exchange_rates(
        adm0_code=adm0_code,
        rate_type=rate_type,
    )
    # convert to datetime
    start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    end_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    # format in df is 23/07/2008
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    return df
