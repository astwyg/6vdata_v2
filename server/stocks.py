import tushare as ts


def get_stocks():
    pro = ts.pro_api()
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name')

    stocks = []
    for _, row in data.iterrows():
        stocks.append({
            "code":row.get("symbol"),
            "name":row.get("name")
        })
    return stocks

if __name__ == "__main__":
    print(get_stocks())