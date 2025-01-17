import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
headers = {"apikey": API_KEY}
filename = "../data/operations.json"


def open_transactions(filename: str) -> Any:
    """
    Функция, которая принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except PermissionError:
        print(f"You don't have permission to read file {filename}.")
        return []
    except json.JSONDecodeError:
        print("Invalid JSON data.")
        return []


# print(open_transactions(filename))


def found_currency(currency: Any) -> Any:
    """
    Функция, которая обращается к API и предоставляет данные о курсах валют
    """
    responce = requests.get(f"https://www.cbr-xml-daily.ru/daily_json.js", headers=headers, timeout=20)
    translate = json.loads(responce.text)
    result = translate["Valute"][currency]["Value"]
    return result


# print(found_currency("USD"))


def sum_transactions(transactions: Any) -> float:
    """
    Функция, которая принимает на вход транзакцию и возвращает сумму транзакции в рублях, возвращает тип float
    """
    all = 0.0
    if transactions.get("operationAmount", {}).get("currency", {}).get("code") == "RUB":
        all += float(transactions["operationAmount"]["amount"])
    elif transactions.get("operationAmount", {}).get("currency", {}).get("code") == "USD":
        all += float(transactions["operationAmount"]["amount"]) * found_currency("USD")
    elif transactions.get("operationAmount", {}).get("currency", {}).get("code") == "EUR":
        all += float(transactions["operationAmount"]["amount"]) * found_currency("EUR")
    return all


transactions = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
}

print(sum_transactions(transactions))
