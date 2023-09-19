from swagger_codegen.api.adapter.requests import RequestsAdapter
from swagger_codegen.api.configuration import Configuration

from twse.client import new_client

if __name__ == "__main__":
    client = new_client(
        adapter=RequestsAdapter(debug=False),
        configuration=Configuration(
            host="https://openapi.twse.com.tw/",
        ),
    )
    print("test")
    stockDayAll = client.trading.get__v1_exchangereport_stock_day_all()
    print(stockDayAll)
    
