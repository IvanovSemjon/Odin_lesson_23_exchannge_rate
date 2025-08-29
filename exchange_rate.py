import requests
import json
import pprint

from tkinter import *
from tkinter import messagebox as mb

# result = requests.get("https://v6.exchangerate-api.com/v6/e48649bb9b00f650443eccb8/latest/USD")
# data = json.loads(result.text)
# p = pprint.PrettyPrinter(indent=4)
# p.pprint(data)

def get_exchange_rate():
    currency = entry.get()
    result = requests.get(f"https://v6.exchangerate-api.com/v6/e48649bb9b00f650443eccb8/latest/{currency}")
    data = json.loads(result.text)
    if data["result"] == "success":
        rate = data["conversion_rates"]["RUB"]
        mb.showinfo("Курс обмена", f"1 {currency} = {rate} RUB")
    else:
        mb.showerror("Ошибка", "Валюта не найдена")

window = Tk()
window.title("Курсы обмена валют")
window.geometry("360x180")

Label(window, text="Введите код валюты:").pack(padx=10, pady=10)

entry = Entry(window)
entry.pack(padx=10, pady=10)

Button(window, text="Получить курс", command=lambda: get_exchange_rate).pack(padx=10, pady=10)