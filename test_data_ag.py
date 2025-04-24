from src.data_ag.ids import ComodityIdsManager, MarketIdsManager, Adm0CodeManager
from src.data_ag.prices import download_prices
from src.data_ag.exchange_rate import download_exchange_rates, get_exchange_rate
from src.data_ag.market import download_market_assessment

if __name__ == "__main__":
    ma = MarketIdsManager()
    ca = ComodityIdsManager()
    aa = Adm0CodeManager()

    all_com_ids = ca.get_all_ids()

    prices = download_prices(
        start_date="2024-04-01",
        end_date="2025-04-30",
        commodity_ids=all_com_ids,
        market_ids=ma.get_market_ids_for_coutry("Ethiopia"),
    )
    print(prices.head())
    print()

    exchange_rates = download_exchange_rates(
        adm0_code=aa.get_code_for_country("Ethiopia"),
        rate_type="Official",
    )

    print(exchange_rates.head())
    print()

    exchange = get_exchange_rate(
        start_date="2024-04-01",
        end_date="2025-04-30",
        adm0_code=aa.get_code_for_country("Ethiopia"),
        rate_type="Official",
    )

    print(exchange.head())
    print()

    market_assess = download_market_assessment(
        adm0_codes=aa.get_code_for_country("Ethiopia"),
        market_ids=ma.get_market_ids_for_coutry("Ethiopia"),
        start_date="2024-04-01",
        end_date="2025-04-30",
    )
    print(market_assess.head())
    print()
