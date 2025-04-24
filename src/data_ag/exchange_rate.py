import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from .utils.cache import cache_csv
from .utils.csv import download_csv


@cache_csv(cache_dir="./cache")
def download_exchange_rates(
    adm0_code: int = 238,
    rate_type: str = "Official",) -> pd.DataFrame:
    """
    Fetches raw exchange-rate CSV for a given country code and rate type.

    Returns a DataFrame with columns ['Date', 'Value', ...].
    """
    url = "https://api.vam.wfp.org/economicExplorer/Currency/ExchangeRateExport"
    payload = {
        "adm0Code": adm0_code,
        "rateType": rate_type,
    }
    return download_csv(url, json=payload)


def get_combined_exchange_rates(
    start_date: str = None,
    end_date: str = None,
    adm0_code: int = 238,
) -> pd.DataFrame:
    """
    Downloads both Official and Parallel rates, merges into one DataFrame with
    columns ['Date', 'Value_official', 'Value_parallel'], optionally filtered by dates.
    """
    # Download raw data
    df_off = download_exchange_rates(adm0_code=adm0_code, rate_type="Official")
    df_par = download_exchange_rates(adm0_code=adm0_code, rate_type="Parallel")

    # Parse dates
    df_off["Date"] = pd.to_datetime(df_off["Date"], format="%d/%m/%Y")
    df_par["Date"] = pd.to_datetime(df_par["Date"], format="%d/%m/%Y")

    # Rename value columns
    df_off = df_off.rename(columns={"Value": "Value_official"})
    df_par = df_par.rename(columns={"Value": "Value_parallel"})

    # Merge on Date
    df = pd.merge(
        df_off[['Date', 'Value_official']],
        df_par[['Date', 'Value_parallel']],
        on='Date', how='outer'
    ).sort_values('Date')

    # Filter by date range if provided
    if start_date is not None and end_date is not None:
        start = pd.to_datetime(start_date, format="%Y-%m-%d")
        end = pd.to_datetime(end_date, format="%Y-%m-%d")
        df = df[(df['Date'] >= start) & (df['Date'] <= end)]

    return df


def preprocess_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resamples combined daily DataFrame into monthly stats:
      - columns: ['Value_official_mean', 'Value_official_min', 'Value_official_max',
                  'Value_parallel_mean', 'Value_parallel_min', 'Value_parallel_max']
    """
    df = df.copy()
    df = df.set_index('Date')

    stats = df.resample('M').agg({
        'Value_official': ['mean', 'min', 'max'],
        'Value_parallel': ['mean', 'min', 'max'],
    })
    # Flatten MultiIndex columns
    stats.columns = [f"{col}_{stat}" for col, stat in stats.columns]
    return stats


def plot_exchange_rate(monthly_df: pd.DataFrame):
    """
    Plots monthly mean ± min/max for both Official and Parallel rates.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # Official
    y_off = monthly_df['Value_official_mean']
    e_low_off = y_off - monthly_df['Value_official_min']
    e_high_off = monthly_df['Value_official_max'] - y_off
    ax.errorbar(
        monthly_df.index, y_off,
        yerr=[e_low_off, e_high_off],
        marker='o', linestyle='-', label='Official'
    )

    # Parallel
    y_par = monthly_df['Value_parallel_mean']
    e_low_par = y_par - monthly_df['Value_parallel_min']
    e_high_par = monthly_df['Value_parallel_max'] - y_par
    ax.errorbar(
        monthly_df.index, y_par,
        yerr=[e_low_par, e_high_par],
        marker='o', linestyle='-', label='Parallel'
    )

    # Formatting
    ax.set_xlabel('Month')
    ax.set_ylabel('Exchange Rate')
    ax.set_title('Monthly Exchange Rates (mean ± min/max)')
    ax.legend()

    # Show every month on x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()
