from typing import Union, List

from .utils.cache import cache_csv
from .utils.csv import download_csv


@cache_csv(cache_dir="./cache")
def download_market_assessment(
    adm0_codes: Union[List[int], int],
    market_ids: Union[List[int], int],
    start_date: str,  # in YYYY-MM-DD format
    end_date: str,  # in YYYY-MM-DD format
):
    """
    Download market assessment data from WFP API.

    Parameters
    ----------
    adm0_codes : Union[List[int], int]
        List of adm0 codes or a single adm0 code.
    market_ids : Union[List[int], int]
        List of market ids or a single market id.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.

    Returns
    -------
    pd.DataFrame
        Market assessment data.
    """
    if isinstance(adm0_codes, int):
        adm0_codes = [adm0_codes]
    if isinstance(market_ids, int):
        market_ids = [market_ids]

    url = "https://api.vam.wfp.org/economicExplorer/MarketFunctionalityIndex/MFIDataExport"
    data = {
        "adm0Codes": adm0_codes,
        "marketIds": market_ids,
        "startDate": start_date,
        "endDate": end_date,
    }

    return download_csv(
        url,
        json=data,
    )
