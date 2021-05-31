import os
import pdb

import pandas as pd
import requests
from dateutil.utils import today
from yahoo_fin import stock_info as si

indexes = {"sp500": si.tickers_sp500,
           "nasdaq": si.tickers_nasdaq,
           "dji": si.tickers_dow}
for name, index in indexes.items():
    tickers = index()
    recommendations = []
    final_tickers = []
    if os.path.exists(f"{name}_{today().strftime('%Y%m%d')}.csv"):
        dataframe = pd.read_csv(f"{name}_{today().strftime('%Y%m%d')}.csv")
        print(dataframe)
    else:
        for ticker in tickers:
            lhs_url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"
            rhs_url = "?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=EU&" \
                      "modules=financialData&corsDomain=finance.yahoo.com"

            url = lhs_url + ticker + rhs_url
            r = requests.get(url)
            if not r.ok:
                recommendation = None
            try:
                result = r.json()["quoteSummary"]["result"][0]
                recommendation = float(result["financialData"]["recommendationMean"]["fmt"])
                print("--------------------------------------------")
                print("{} has an average recommendation of: ".format(ticker), recommendation)
            except:
                recommendation = None

            if recommendation:
                final_tickers.append(ticker)
                recommendations.append(recommendation)

        dataframe = pd.DataFrame(list(zip(final_tickers, recommendations)), columns=["Company", "Recommendations"])
        dataframe = dataframe.set_index("Company")
        dataframe.to_csv(f"{name}_{today().strftime('%Y%m%d')}.csv")
        print(dataframe)
