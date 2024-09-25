import datetime
import requests
import os.path
import csv
import datetime as dt

base_url = "https://api.bybit.com"
fetch_ohlc = base_url + "/v5/market/kline"
open_interest = base_url + "/v5/market/open-interest"

def obtain_historical_data(url, category, symbol, interval, limit):
    """
    Function that creates a csv file or adds to an existing one from what is returned when querying bybit for market
    information on the provided symbol you pass in, it specifically returns the ohlc for that symbol as well as the
    volume and the timeframe. For more information visit https://bybit-exchange.github.io/docs/v5/market/kline
    :param url: The url needed to reach the market data through the bybit api
    :param category: a string containing the value of the product type i.e "linear", "spot", "inverse" type of contract
    :param symbol: a string containing the assets symbol i.e "BTCUSDT"
    :param interval: a string containing the timeframe to return ohcl from i.e "1", "15", "60", "240", "D", "W","M"
    :param limit: an integer, the amount of results to return (max=1000)
    """

    # The dictionary of parameters to pass into the api request
    params = {"category": category,
              "symbol": symbol,
              "interval": interval,
              "limit": limit
              }

    r = requests.get(url, params=params)

    # File name for our csv output
    file_name = f"{symbol}-{interval}.csv"

    # Check to see if the file exists, if it doesn't, then create it and add the column headers
    if not os.path.exists(file_name):
        new_file = open(file_name, "w")
        new_file.write("date,time,open,high,low,close,volume\n")
        new_file.close()

    # Create a new list from the requested data to easily split up below, reverse the data so the time counts forward
    entry = [x for x in r.json()["result"]["list"]]
    entry.reverse()

    # Open the csv file
    with open(file_name, "a", newline="") as csvfile:
        # Create a writer
        writer = csv.writer(csvfile, delimiter=",")

        # Iterate through each entry returned
        for x in entry:
            # Assign the correct values for every slice of the returned list
            t = int(x[0])/1000
            d = dt.datetime.fromtimestamp(t, datetime.UTC).strftime("%a-%d-%b-%y")
            t = dt.datetime.fromtimestamp(t, datetime.UTC).strftime("%H:%M:%S")

            o = round(float(x[1]))
            h = round(float(x[2]))
            l = round(float(x[3]))
            c = round(float(x[4]))

            # Volume returns in traded currency units, so multiplying it by the average price for the time period should
            # Give an accurate representation
            v = round(float(x[5])) * o - c

            # Write all the variables to a row in the csv
            writer.writerow([d, t, o, h, l, c, v])

def get_open_interest(url: str, category: str, symbol: str, timeframe: str, limit: int) -> None:
    parameters: dict = {"category": category,
                        "symbol": symbol,
                        "intervalTime": timeframe,
                        "limit": limit}

    r = requests.get(url, params=parameters)
    results = r.json()
    print(results)


# Fetch the ohlc for the day on the 15minute time frame
# obtain_historical_data(fetch_ohlc, "linear", "BTCUSDT", "15", 1000)
# # Fetch the ohlc for the day on the 1hour time frame
# obtain_historical_data(fetch_ohlc, "linear", "BTCUSDT", "60", 1000)
# # Fetch the ohlc for the day on the 1hour time frame
# obtain_historical_data(fetch_ohlc, "linear", "BTCUSDT", "240", 1000)
# Fetch the ohlc for the day on the 1hour time frame
# obtain_historical_data(fetch_ohlc, "linear", "BTCUSDT", "D", 1)

get_open_interest(open_interest, "linear", "BTCUSDT", "1", 50)
