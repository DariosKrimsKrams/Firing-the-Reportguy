import requests
import pandas as pd
from typing import List, Dict
import io

from .utils.constants import ALL_COMMODITIES
from .utils.cache import cache_csv
from .utils.constants import ADM0CODEData


@cache_csv(cache_dir="./cache")
def download_market_ids() -> pd.DataFrame:
    """
    Download market ids and commodity ids from WFP API and return as DataFrame.

    Parameters:
        comodity_list (dict): JSON payload for filtering commodities.
    """
    url = "https://api.vam.wfp.org/economicExplorer/Markets/MarketFlatListExport"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    response = requests.post(url, headers=headers, json=ALL_COMMODITIES)
    response.raise_for_status()
    # Read CSV content into DataFrame
    df = pd.read_csv(io.StringIO(response.text))
    return df


@cache_csv(cache_dir="./cache")
def downlaod_comodity_ids():
    """
    download the market ids and comodity ids
    """
    url = "https://api.vam.wfp.org/economicExplorer/Commodities/GetAllCommodityExport"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15",
    }
    response = requests.post(url, headers=headers, json=ALL_COMMODITIES)
    response.raise_for_status()
    # Read CSV content into DataFrame
    df = pd.read_csv(io.StringIO(response.text))
    return df


class MarketIdsManager:
    def __init__(self):
        self.df = download_market_ids()
        # Columns: MarketId      Country     Admin 1        Admin 2 Market Name  Latitude  Longitude  Population

    @property
    def columns(self):
        return self.df.columns

    def get_market_ids_for_coutry(self, country: str) -> List[int]:
        return self.df[self.df["Country"] == country]["MarketId"].tolist()

    def get_info_for_id(self, id: int) -> Dict[str, str]:
        """
        returns dict
            "country": "country",
            "region": "region",
        """
        pass


class ComodityIdsManager:
    def __init__(self):
        self.df = downlaod_comodity_ids()
        # Columns: Id                     Name

    @property
    def columns(self):
        return self.df.columns

    def get_comodity_id_for_group(self, group: str) -> int:
        ids_list = self.df[self.df["Name"] == group]["Id"].tolist()
        assert len(ids_list) == 1, f"Weird group name {group} with ids {ids_list}"
        return ids_list[0]

    def get_comodity_name_for_id(self, id: int) -> str:
        names_list = self.df[self.df["Id"] == id]["Name"].tolist()
        assert len(names_list) == 1, f"Weird id {id} with names {names_list}"
        return names_list[0]

    def get_all_ids(self) -> List[int]:
        return self.df["Id"].tolist()


class Adm0CodeManager:
    def __init__(self):
        self.data = self._generate_data()

    def _generate_data(self):
        data = {}
        for line in ADM0CODEData.strip().splitlines():
            id_str, name, y1, y2 = line.split("\t")
            data[int(id_str)] = {"name": name, "year1": int(y1), "year2": int(y2)}
        return data

    def get_code_for_country(self, country_name):
        for code, info in self.data.items():
            if info["name"].lower() == country_name.lower():
                return code
        raise ValueError(f"Country '{country_name}' not found in ADM0CODE data.")

    def get_country_for_code(self, code):
        if code in self.data:
            return self.data[code]["name"]
        raise ValueError(f"Code '{code}' not found in ADM0CODE data.")
