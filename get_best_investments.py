import os
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
    prices = []
    price_mean_targets = []
    price_min_targets = []
    price_diffs = []
    projected_returns = []
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
                price = float(result["financialData"]["currentPrice"]["fmt"])
                price_mean_target = float(result["financialData"]["targetMeanPrice"]["fmt"])
                price_min_target = float(result["financialData"]["targetLowPrice"]["fmt"])
                price_mean_diff = round(price - price_mean_target, 2)
                projected_min_return = round(price_min_target/price, 2)
                print("--------------------------------------------")
                print("{} has an average recommendation of: ".format(ticker), recommendation)
            except:
                recommendation = None
                price = None
                price_mean_target = None
                price_min_target = None
                price_mean_diff = None
                projected_min_return = None

            if recommendation:
                final_tickers.append(ticker)
                recommendations.append(recommendation)
                prices.append(price)
                price_mean_targets.append(price_mean_target)
                price_min_targets.append(price_min_target)
                price_diffs.append(price_mean_diff)
                projected_returns.append(projected_min_return)

        dataframe = pd.DataFrame(list(zip(final_tickers,
                                          recommendations,
                                          prices,
                                          price_mean_targets,
                                          price_min_targets,
                                          price_diffs,
                                          projected_returns)),
                                 columns=["Company",
                                          "Recommendations",
                                          "Price",
                                          "Price Mean Target",
                                          "Price Min. Target",
                                          "Price To Target Difference",
                                          "Projected Returns"])
        dataframe = dataframe.set_index("Company")
        dataframe.to_csv(f"{name}_{today().strftime('%Y%m%d')}.csv")
        print(dataframe)
