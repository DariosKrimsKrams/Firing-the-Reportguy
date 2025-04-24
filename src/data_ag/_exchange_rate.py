import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

    if start_date is None or end_date is None:
        return df
    # convert to datetime
    start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    end_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    # format in df is 23/07/2008
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    return df

def preprocess_monthly(df, date_col='Date', value_col='Value'):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], dayfirst=True)
    df.set_index(date_col, inplace=True)
    return df[value_col].resample('M').agg(['mean','min','max'])


def plot_exchange_rate(
    official_monthly: pd.DataFrame,
    parallel_monthly: pd.DataFrame,
):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Official
    y_off = official_monthly['mean']
    err_off = [y_off - official_monthly['min'], official_monthly['max'] - y_off]
    ax.errorbar(
        official_monthly.index, y_off,
        yerr=err_off,
        marker='o', linestyle='-',
        label='Official'
    )

    # Parallel
    y_par = parallel_monthly['mean']
    err_par = [y_par - parallel_monthly['min'], parallel_monthly['max'] - y_par]
    ax.errorbar(
        parallel_monthly.index, y_par,
        yerr=err_par,
        marker='o', linestyle='-',
        label='Parallel'
    )

    # formatting
    ax.set_xlabel('Month')
    ax.set_ylabel('Exchange Rate')
    ax.set_title('Monthly Exchange Rates (mean ± min/max)')
    ax.legend()

    # <— NEW: show every month on the x–axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())              # one tick per month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))    # e.g. "Apr 2025"

    fig.autofmt_xdate()   # rotate & align
    plt.tight_layout()
    plt.show()
