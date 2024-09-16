# Import statements
import requests

# base url to query
base_url = "https://www.bitmex.com/api/v1"


def get_current_price(base):
    """
    A function that returns the current price of XBTUSDT (BTC/TETHER) from
    bitmex using the requests library
    :param base: The base url for bitmex, needed to access the api
    :return: the current price of btcusdt from the bitmex tether perpetual contract
    """

    # Create the url to query price using the base url provided as well as the specific location of the bid
    get_quote = base + "/quote"

    # Create a dictionary of parameters to pass into the api
    current_price_params = {"symbol": "XBTUSDT",
                            "reverse": True,
                            "columns": "bidPrice, askPrice"
                            }

    # Create a requests object passing it the url and the parameters dictionary
    r = requests.get(get_quote, current_price_params)

    # Slice out the bid price from the json returned from the request
    bid = r.json()[0]["bidPrice"]

    print(f"The current price of bitcoin is: ${round(bid):,.2f}")

    return int(bid)


def get_specific_timeframe_quote(base):
    url = base+"/quote/bucketed"

    r = requests.get()

    return None

# current_btc_price = get_current_price(base_url)

# one_min_params = {"binSize": "1m",
#                   "symbol": "XBTUSDT",
#                   "reverse": True,
#                   }
#
# r = requests.get(base_url+"/quote/bucketed", params= one_min_params)
#
# print(r.json())

