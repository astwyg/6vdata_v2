import os
import tushare as ts
import requests.exceptions
import pandas as pd

from conf.conf import get_conf
from conf.log import server_logger

def get_stocks():
    try:
        ts.set_token(get_conf("tushare_token"))
        pro = ts.pro_api()
        data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name')
        server_logger.debug("stock data fetched {}".format(len(data)))
        data.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',"data","stocks.csv"), encoding="utf-8")
    except Exception:
        data = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',"data","stocks.csv"), encoding = "utf-8")
        server_logger.warning("tushare connect failed , data from local storage")

    stocks = []
    for _, row in data.iterrows():
        stocks.append({
            "code":row.get("symbol"),
            "name":row.get("name")
        })
    return stocks

if __name__ == "__main__":
    print(get_stocks())