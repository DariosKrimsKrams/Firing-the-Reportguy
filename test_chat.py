from src.llm.model import Model
from src.data_ag.exchange_rate import get_exchange_rate
from src.data_ag.ids import Adm0CodeManager

def fake_function(start_date: str, end_date: str, y_axis: str):
    print(f"Plotting data from {start_date} to {end_date} for {y_axis}")

if __name__ == "__main__":
    model = Model()

    # model.register_function_call(
    #     {
    #         "type": "function",
    #         "name": "plot_data",
    #         "description": "Plot some data, so the user can see what you are talking about.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format."},
    #                 "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format."},
    #                 "y_axis": {"type": "string", "description": "The y-axis variable to plot."},
    #             },
    #             "additionalProperties": False
    #         },
    #     },
    #     fake_function
    # )

    adm_manager = Adm0CodeManager()

    exchnage_rate_df = get_exchange_rate(
        start_date="2023-01-01",
        end_date="2025-04-30",
        adm0_code=adm_manager.get_code_for_country("Syrian Arab Republic")
    )

    res = model.run_for_df(exchnage_rate_df)
    print(res)

    
