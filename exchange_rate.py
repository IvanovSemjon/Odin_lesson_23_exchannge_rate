import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb


def update_c_lable(event):
    code = combobox.get()
    name = cur[code]
    c_label.configure(text=f"{code} - {name}")



def get_exchange_rate():
    currency = combobox.get()

    if currency:
        try:
            response = requests.get(f"https://v6.exchangerate-api.com/v6/e48649bb9b00f650443eccb8/latest/USD")
            response.raise_for_status()
            data = response.json()
            if currency in data["conversion_rates"]:
                exchange_rate = data["conversion_rates"][currency]
                c_name = cur[currency]
                mb.showinfo("Курс обмена", f"Курс: {exchange_rate:.2f} {c_name} за один доллар.")
            else:
                mb.showerror("Ошибка", "Валюта не найдена")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка --> {e}")
    else:
        mb.showwarning("Ошибка", "Введите код валюты")


cur = {
    "USD": "Американский доллар", 
    "EUR": "Евро",
    "BYN": "Белорусский рубль", 
    "AZN": "Азербайджанский манат",
    "AMD": "Армянский драм",
    "BGN": "Болгарский лев",
    "INR": "Индийская рупия",
    "KZT": "Казахстанский тенге",
    "CNY": "Китайский юань",
    "BRL": "Бразильский реал",
    "RUB": "Российский рубль"
    }


window = Tk()
window.title("Курсы обмена валют")
window.geometry("360x180")

Label(text="Выберите код валюты:").pack(padx=10, pady=10)
combobox = ttk.Combobox(values=list(cur.keys()))
combobox.pack(padx=10, pady=10)
combobox.bind("<<ComboboxSelected>>", update_c_lable)

c_label = ttk.Label()
c_label.pack(padx=10, pady=10)

Button(text="Получить курс", command=get_exchange_rate).pack(padx=10, pady=10)

window.mainloop()