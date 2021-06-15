import os

import pandas as pd
import requests
from dateutil.utils import today
from yahoo_fin import stock_info as si

invested_in = {"invested": ["ADMA", "BTAI", "IMUX", "IMVT", "OPTN", "PRQR", "SIOX", "VKTX"]}
indexes = {"nasdaq": si.tickers_nasdaq()}
for name, index in invested_in.items():
    tickers = index
    recommendations = []
    final_tickers = []
    prices = []
    price_mean_targets = []
    price_min_targets = []
    price_diffs = []
    projected_min_returns = []
    projected_mean_returns = []
    n_of_analysts = []
    if os.path.exists(f"{name}_{today().strftime('%Y%m%d')}.csv"):
        dataframe = pd.read_csv(f"{name}_{today().strftime('%Y%m%d')}.csv")
        dataframe = dataframe.round(2)
        print(dataframe)
        dataframe.to_csv(f"{name}_{today().strftime('%Y%m%d')}.csv")
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
                projected_mean_return = round(price_mean_target / price, 2)
                projected_min_return = round(price_min_target / price, 2)
                n_analysts = result["financialData"]["numberOfAnalystOpinions"]["raw"]
                print("--------------------------------------------")
                print(f"{ticker} has an average recommendation of: {recommendation} by {n_analysts} analysts")
            except:
                recommendation = None
                price = None
                price_mean_target = None
                price_min_target = None
                price_mean_diff = None
                projected_mean_return = None
                projected_min_return = None
                n_analysts = None

            if recommendation:
                final_tickers.append(ticker)
                recommendations.append(recommendation)
                prices.append(price)
                price_mean_targets.append(price_mean_target)
                price_min_targets.append(price_min_target)
                price_diffs.append(price_mean_diff)
                projected_mean_returns.append(projected_mean_return)
                projected_min_returns.append(projected_min_return)
                n_of_analysts.append(n_analysts)

        dataframe = pd.DataFrame(list(zip(final_tickers,
                                          recommendations,
                                          prices,
                                          price_mean_targets,
                                          price_min_targets,
                                          price_diffs,
                                          projected_min_returns,
                                          projected_mean_returns,
                                          n_of_analysts)),
                                 columns=["Company",
                                          "Recommendations",
                                          "Price",
                                          "Price Mean Target",
                                          "Price Min. Target",
                                          "Price To Target Difference",
                                          "Projected Minimum Returns",
                                          "Projected Mean Returns",
                                          "Number of Analysts"])
        dataframe = dataframe.set_index("Company")
        dataframe.to_csv(f"{name}_{today().strftime('%Y%m%d')}.csv")
        print(dataframe)
