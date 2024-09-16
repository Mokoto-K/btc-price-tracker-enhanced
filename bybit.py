import requests
import csv

base_url = "https://api.bybit.com"
fetch_ohlc = base_url+"/v5/market/kline"


def the_function(url, category, symbol, interval, limit):
    """
    Function that creates a csv file or adds to an existing one from what is returned when querying bybit for market
    information on the provided symbol you pass in, it specifically returns the ohlc for that symbol as well as the
    volume and the timeframe. For more information visit https://bybit-exchange.github.io/docs/v5/market/kline
    :param url: The url needed to reach the market data through the bybit api
    :param category: a string containing the value of the product type i.e "linear", "spot", "inverse" type of contract
    :param symbol: a string containing the assets symbol i.e "BTCUSDT"
    :param interval: a string containing the timeframe to return ohcl from i.e "1", "15", "60", "240", "D", "W","M"
    :param limit: an integer, the amount of results to return
    """

    # The dictionary of parameters to pass into the api request
    params = {"category": category,
              "symbol": symbol,
              "interval": interval,
              "limit": limit
              }

    r = requests.get(url, params=params)

    # File name for our csv oupt
    file_name = f"{symbol}-{interval}.csv"

    try:
        with open(file_name, "r") as csvfile:
            None

    except (FileNotFoundError):
        new_file = open(file_name, "w")
        new_file.write("time,open,high,low,close,volume")

    # Create a new list from the requested data to easily split up below
    entry = [x for x in r.json()["result"]["list"]]

    edited_entries = []

    # Open or create a csv file
    with open(file_name, "a", newline="") as csvfile:

        writer = csv.writer(csvfile, delimiter=",")
        # Iterate through each entry returned
        for x in entry:
            # Assign the correct values for every slice of the returned list
            t = x[0]
            o = round(float(x[1]))
            h = round(float(x[2]))
            l = round(float(x[3]))
            c = round(float(x[4]))

            # Volume returns in traded currency units, so multiplying it by the average price for the time period should
            # Give an accurate representation

            v = round(float(x[5])) * o - c

            writer.writerows()

# Fetch the ohlc for the day on the 15minute time frame
the_function(fetch_ohlc, "linear", "BTCUSDT", "15", 96)

