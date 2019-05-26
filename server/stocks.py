import tushare as ts
from conf.conf import get_conf

from conf.log import server_logger

def get_stocks():
    ts.set_token(get_conf("tushare_token"))
    pro = ts.pro_api()
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name')

    server_logger.debug("stock data fetched {}".format(len(data)))

    stocks = []
    for _, row in data.iterrows():
        stocks.append({
            "code":row.get("symbol"),
            "name":row.get("name")
        })
    return stocks

if __name__ == "__main__":
    print(get_stocks())