import requests
from tkinter import *
from tkinter import messagebox as mb


def get_exchange_rate():
    currency = entry.get()

    if currency:
        try:
            currency = currency.upper()
            response = requests.get(f"https://v6.exchangerate-api.com/v6/e48649bb9b00f650443eccb8/latest/{currency}")
            response.raise_for_status()
            data = response.json()
            if currency in data["conversion_rates"]:
                exchange_rate = data["conversion_rates"][currency]
                mb.showinfo("Курс обмена", f"Курс: {exchange_rate} {currency} за один доллар.")
            else:
                mb.showerror("Ошибка", "Валюта не найдена")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка --> {e}")
    else:
        mb.showwarning("Ошибка", "Введите код валюты")


window = Tk()
window.title("Курсы обмена валют")
window.geometry("360x180")

Label(window, text="Введите код валюты:").pack(padx=10, pady=10)

entry = Entry(window)
entry.pack(padx=10, pady=10)

Button(window, text="Получить курс", command=lambda: get_exchange_rate).pack(padx=10, pady=10)

window.mainloop()