#from getpass import getpass
#
#API_KEY = getpass("Please input your AlphaVantage API Key: ")


import requests
import json
from pprint import pprint
from statistics import mean
from plotly.express import line


from app.alpha import API_KEY


def format_pct(my_number):
    """
    Formats a percentage number like 3.6555554 as percent, rounded to two decimal places.

    Param my_number (float) like 3.6555554

    Returns (str) like '3.66%'
    """
    return f"{my_number:.2f}%"


def fetch_unemployment_data():
    """Fetches unemployment data from the AlphaVantage API.
        Returns data as a list of dictionaries, where each represents the unemployment rate for a given month.
        Formats rates as floats.
    """

    request_url = f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={API_KEY}"

    response = requests.get(request_url)

    parsed_response = json.loads(response.text)
    print(type(parsed_response))
    pprint(parsed_response)

    data = parsed_response["data"]

    # we could return the raw data, but the values are strings,
    # so let's convert them to floats (more usable) before returning
    for d in data:
        d["value"] = float(d["value"]) # this is mutating and will overwrite the data

    return data



if __name__ == "__main__":

    # only run the code below if we run this file from the command line
    # otherwise if we are just importing some functions from this file
    # don't run this code

    data = fetch_unemployment_data()


    # Challenge A
    #
    # What is the most recent unemployment rate? And the corresponding date?
    # Display the unemployment rate using a percent sign.

    print("-------------------------")
    print("LATEST UNEMPLOYMENT RATE:")
    #print(data[0])
    #print(f"{data[0]['value']}%", "as of", data[0]["date"])
    print(format_pct(data[0]['value']), "as of", data[0]["date"])



    # Challenge B
    #
    # What is the average unemployment rate for all months during this calendar year?
    # ... How many months does this cover?


    this_year = [d for d in data if "2023-" in d["date"]]

    rates_this_year = [d["value"] for d in this_year]
    #print(rates_this_year)

    print("-------------------------")
    #print("AVG UNEMPLOYMENT THIS YEAR:", f"{mean(rates_this_year)}%")
    print("AVG UNEMPLOYMENT THIS YEAR:", f"{format_pct(mean(rates_this_year))}")
    print("NO MONTHS:", len(this_year))


    # Challenge C
    #
    # Plot a line chart of unemployment rates over time.


    dates = [d["date"] for d in data]
    rates = [d["value"] for d in data]

    fig = line(x=dates, y=rates, title="United States Unemployment Rate over time", labels= {"x": "Month", "y": "Unemployment Rate"})
    fig.show()
