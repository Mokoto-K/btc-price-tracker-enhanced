# Create a dictionary to hold all of our days of the week and their values
price_dictionary = {}

# Open a csv file containing our prices
with open("./BTCUSDT-D.csv", "r") as data:
    # Read in all of the lines from the csv
    line_reader = data.readlines()
    line_reader.pop(0)

    # Iterate over each line
    for line in line_reader:

        # Split the elements up and assign them to their correct variables
        elements = line.split(",")
        date = elements[0]
        time = elements[1]
        open_price = round(float(elements[2]))
        high_price = round(float(elements[3]))
        low_price = round(float(elements[4]))
        close_price = round(float(elements[5]))
        volume = int(elements[6])

        # Calculate a set of features to be used
        day = date.replace('"', '').split("-")[0]
        difference = round(close_price * 100 / open_price - 100, 2)
        high_to_close = round((high_price - close_price) * 100 / close_price, 2)
        low_to_close = round((close_price - low_price) * 100 / close_price, 2)
        high_to_low = round((high_price - low_price) * 100 / high_price, 2)

        # Place all the features into a list
        price_metrics = [difference, high_to_close, low_to_close, high_to_low]

        # If a day of the week isnt in the dictionary, add it with the first set of metrics as its value
        if not day in price_dictionary.keys():
            price_dictionary[day] = [price_metrics]
        # If the day is a key in the dictionary, add the next round of metrics to the values as another list
        else:
            price_dictionary[day].append(price_metrics)


def function(day, values):
    """

    :param day: Key of a dictionary containing a day of the week
    :param values: a list containing a lists of each days metrics for price
    """

    # Initiate our variables to keep track of the metrics totals
    difference, diff_div = 0, 0
    high_to_close, high_div = 0, 0
    low_to_close, low_div = 0, 0
    high_to_low, mag_div = 0, 0

    threshold = 10

    # Iterate over every list in the list
    for num in values:
        difference += num[0]
        high_to_close += num[1]
        low_to_close += num[2]
        high_to_low += num[3]

        # Only add entries that are inside the threshold
        # if threshold > num[0] > -threshold:
        #     difference += num[0]
        #     diff_div += 1
        # if threshold > num[1] > -threshold:
        #     high_to_close += num[1]
        #     high_div += 1
        # if threshold > num[2] > -threshold:
        #     low_to_close += num[2]
        #     low_div += 1
        # if threshold > num[3] > -threshold:
        #     high_to_low += num[3]
        #     mag_div += 1

    # divide the totals by the amount of entries and round the answer
    # difference = round(difference/diff_div,2)
    # high_to_close = round(high_to_close/high_div,2)
    # low_to_close = round(low_to_close/low_div,2)
    # high_to_low = round(high_to_low/mag_div,2)

    difference = round(difference / len(values), 2)
    high_to_close = round(high_to_close / len(values), 2)
    low_to_close = round(low_to_close / len(values), 2)
    high_to_low = round(high_to_low / len(values), 2)

    print(f"{day}\t Change: {difference}\t High: {high_to_close}\t Low: {low_to_close}\t Magnitude: {high_to_low}")

# Iterate over each key in the price dictionay and call the price function to get each days stats
for key, value in price_dictionary.items():
    function(key, value)


profit = 0
for day in price_dictionary["Mon"]:
    profit += day[0]

print(profit)

