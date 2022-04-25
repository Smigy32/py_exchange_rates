from datetime import date, timedelta
import csv
import json

import requests
from matplotlib import pyplot as plt


def graphs(func):
    """
    The decorator builds a graph of exchange rates for some date range
    :param func: Any function that returns a list with exchanging rates and their dates
    """
    def wrapper(*args, **kwargs):
        rates = func(*args, **kwargs)
        fig, ax = plt.subplots()
        x = [rate["date"] for rate in rates]
        y = [rate["rate"] for rate in rates]
        ax.plot(x, y)
        plt.show()
        return rates

    return wrapper


def get_nbu_exchange_rates(valcode, start_date: date, end_date: date = None, to_csv=False, to_json=False):
    """
    Get information about NBU exchange rates for some date range
    :param valcode: Currency code
    :param start_date: Start date of needed date range
    :param end_date: End date of needed date range
    :param to_csv: If this param's True the result will be written into a csv file
    :param to_json: If this param's True the result will be written into a json file
    :return: rates - list that consists of exchange rates
    """

    start_date_f = int(start_date.strftime("%Y%m%d"))  # convert start date into an int
    rates = []  # list that will store the result
    if end_date:
        end_date_f = int(end_date.strftime("%Y%m%d"))  # convert end date into an int
        for ex_date in range(start_date_f, end_date_f + 1):
            general_info = requests.get(
                f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={valcode}&"
                f"date={ex_date}&json").json()  # all info about the currency

            rates.append({  # convert the data into a readable dict and add it to the result list
                "date": general_info[0]["exchangedate"],
                "currency": valcode,
                "rate": general_info[0]["rate"],
            })
    else:
        general_info = requests.get(
            f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={valcode}&"
            f"date={start_date_f}&json").json()  # all info about the currency

        rates.append({  # convert the data into a readable dict and add it to the result list
            "date": general_info[0]["exchangedate"],
            "currency": valcode,
            "rate": general_info[0]["rate"],
        })

    if to_csv:
        with open('rates_nbu.csv', 'w') as csv_file:
            fieldnames = ['date', 'currency', 'rate']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(rates)

    if to_json:
        with open("rates_nbu.json", "w") as json_file:
            json.dump(rates, json_file)

    return rates


def get_pb_exchange_rates(valcode: str, start_date: date, end_date: date = None, to_csv=False, to_json=False):
    """
    Get information about PrivatBank exchange rates for some date range
    :param valcode: Currency code
    :param start_date: Start date of needed date range
    :param end_date: End date of needed date range
    :param to_csv: If this param's True the result will be written into a csv file
    :param to_json: If this param's True the result will be written into a json file
    :return: rates - list that consists of exchange rates
    """

    valcode = valcode.upper()
    rates = []  # list that will store the result
    if end_date:
        duration = end_date - start_date  # find range of days
        for day in range(duration.days + 1):
            current_date = (start_date + timedelta(days=day)).strftime("%d.%m.%Y")
            general_info = requests.get(
                f"https://api.privatbank.ua/p24api/exchange_rates?json&date={current_date}").json()  # full info

            for cur_info in general_info["exchangeRate"][1:]:
                if cur_info["currency"] == valcode:  # we need a rate only for the currency in params
                    rates.append({  # convert the data into a readable dict and add it to the result list
                        "date": current_date,
                        "currency": valcode,
                        "rate": cur_info["saleRate"],
                    })
    else:
        start_date_f = start_date.strftime("%d.%m.%Y")
        general_info = requests.get(
            f"https://api.privatbank.ua/p24api/exchange_rates?json&date={start_date_f}").json()

        for cur_info in general_info["exchangeRate"][1:]:
            if cur_info["currency"] == valcode:
                rates.append({  # convert the data into a readable dict and add it to the result list
                    "date": start_date_f,
                    "currency": valcode,
                    "rate": cur_info["saleRate"],
                })

    if to_csv:
        with open('rates_pb.csv', 'w') as csv_file:
            fieldnames = ['date', 'currency', 'rate']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(rates)

    if to_json:
        with open("rates_pb.json", "w") as json_file:
            json.dump(rates, json_file)

    return rates


def graph_of_exchange_rates(valcode: str, start_date: date, end_date: date):
    """
    The function builds a graph of NBU and PrivatBank exchange rates for some date range
    :param valcode: Currency code
    :param start_date: Start date of needed date range
    :param end_date: End date of needed date range
    """
    nbu_rates = get_nbu_exchange_rates(valcode, start_date, end_date)  # get nbu rates
    pb_rates = get_pb_exchange_rates(valcode, start_date, end_date)  # get privatbank rates

    fig, ax = plt.subplots()
    dates = [rate["date"] for rate in nbu_rates]  # list of dates (x-axis)
    pb = [rate["rate"] for rate in pb_rates]  # list of pb rates (y-axis)
    nbu = [rate["rate"] for rate in nbu_rates]  # list of nbu rates (y-axis)
    plt.plot(dates, nbu, marker="o", label="NBU")  # build a graph for nbu rates
    plt.plot(dates, pb, marker="o", label="PrivatBank")  # build a graph for pb rates

    plt.xlabel("Dates", fontsize=14)
    plt.ylabel("Rates", fontsize=14)

    plt.legend(loc="best")

    plt.show()


result_nbu = get_nbu_exchange_rates("EUR", date(day=20, month=4, year=2022), date(day=24, month=4, year=2022))
result_pb = get_pb_exchange_rates("EUR", date(day=20, month=4, year=2022), date(day=24, month=4, year=2022))
print(result_nbu)
print(result_pb)


graph_of_exchange_rates("EUR", date(day=20, month=4, year=2022), date(day=24, month=4, year=2022))