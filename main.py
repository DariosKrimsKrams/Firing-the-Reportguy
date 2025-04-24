from src.llm.model import Model
from src.llm.fakechat_gpt_ui import FakeModel
from src.data_ag.exchange_rate import get_combined_exchange_rates
from src.data_ag.market import download_market_assessment
from src.data_ag.prices import download_prices
from src.data_ag.ids import Adm0CodeManager, ComodityIdsManager, MarketIdsManager
import pandas as pd


def filter_comm(df, commodities):
    df_filt = df[df['Commodity'].isin(commodities)].copy()
    
    # 2. Parse dates and floor to month
    df_filt['Price Date'] = pd.to_datetime(df_filt['Price Date'], dayfirst=True)
    df_filt['Month'] = df_filt['Price Date'].dt.to_period('M').dt.to_timestamp()
    
    # 3. Group & average
    monthly = (
        df_filt
        .groupby(['Month', 'Commodity', 'Country'])['Price']
        .mean()
        .reset_index()
        .pivot(index='Month', columns='Commodity', values='Price')
        .sort_index()
    )

    return monthly



def main(country_name: str = "Syrian Arab Republic", start_date: str = "2023-01-01", end_date: str = "2025-04-30"):
    # get all the data
    adm_manager = Adm0CodeManager()
    comodity_manager = ComodityIdsManager()
    market_manager = MarketIdsManager()

    adm0 = adm_manager.get_code_for_country(country_name)
    market_ids = market_manager.get_market_ids_for_coutry(country_name)
    comodity_ids = comodity_manager.get_all_ids()

    exchange_rate_df = get_combined_exchange_rates(
        start_date=start_date,
        end_date=end_date,
        adm0_code=adm0,
    )

    prices_data = download_prices(
        start_date=start_date,
        end_date=end_date,
        market_ids=market_ids,
        commodity_ids=comodity_ids,
    )

    commodities = [
        "Sugar",
        "Water (drinking)",
        "Wheat flour",
        "Eggs",
    ]

    # filter prices daata to have "Commodity" in commodities
    # prices_data = prices_data[prices_data["Commodity"].isin(commodities)]
    prices_data = filter_comm(prices_data, commodities)
    

    # # drop columns
    # cols_to_keep = ['Country', 'Market Name', 'Commodity',
    #    'Price Type', 'Price Date', 'Collection Frequency', 'Price', 'Unit',
    #    'Currency', 'Data Source']
    # prices_data = prices_data[cols_to_keep]

    # market 
    market_ass = download_market_assessment(
        adm0_codes=[adm0],
        market_ids=market_ids,
        start_date=start_date,
        end_date=end_date,
    )


    dfs = {
        "Exchange Rate": exchange_rate_df,
        "Commodities": prices_data,
        "Markets": market_ass
    }

    resulst = {}


    # init model
    model = FakeModel()

    for name, df in dfs.items():
        answer = model.run_for_df(df)
        resulst[name] = answer
        print(f"Answer for {name}:")
        print(answer)
        print("\n" + "="*50 + "\n")

        # TODO plot


    # save the results to a file
    import json
    with open("./results.json", "w") as f:
        json.dump(resulst, f, indent=4)





if __name__ == "__main__":
    main()