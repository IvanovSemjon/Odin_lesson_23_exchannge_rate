import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb


def update_c_lable(event):
    code = target_combobox.get()
    name = cur[code]
    target_label.config(text=f"{name}")
    base_label.config(text=f"{name}")



def get_exchange_rate():
    base_code = base_combobox.get()
    target_code = target_combobox.get()
    
    if target_code and base_code:
        try:
            response = requests.get(f"https://v6.exchangerate-api.com/v6/e48649bb9b00f650443eccb8/latest/{base_code}")
            response.raise_for_status()
            data = response.json()
            if target_code in data["conversion_rates"]:
                exchange_rate = data["conversion_rates"][target_code]
                target_name = cur[target_code]
                base_name = cur[base_code]
                mb.showinfo("Курс обмена", f"Один {base_name} равняется: {exchange_rate:.2f} {target_name}.")
            else:
                mb.showerror("Ошибка", f"Валюта {target_code} не найдена")
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
window.geometry("360x300")


Label(text="Базовая валюта").pack(padx=10, pady=10)
base_combobox = ttk.Combobox(values=list(cur.keys()), width=40)
base_combobox.pack(padx=10, pady=10)
base_combobox.bind("<<ComboboxSelected>>", update_c_lable)

base_label = ttk.Label()
base_label.pack(padx=10, pady=10)


Label(text="Целевая валюта:").pack(padx=10, pady=10)
target_combobox = ttk.Combobox(values=list(cur.keys()), width=40)
target_combobox.pack(padx=10, pady=10)
target_combobox.bind("<<ComboboxSelected>>", update_c_lable)

target_label = ttk.Label()
target_label.pack(padx=10, pady=10)



Button(text="Получить курс", command=get_exchange_rate).pack(padx=10, pady=10)

window.mainloop()