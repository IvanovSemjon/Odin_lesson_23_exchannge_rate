import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb


def update_c_label(event):
    """Обновление меток с названиями валют"""
    try:
        # Для базовой валюты
        if event.widget == base_combobox:
            base_code = base_combobox.get()
            if base_code in cur:
                base_name = cur[base_code]
                base_label.config(text=f"Выбрано: {base_name}")
            else:
                base_label.config(text="")
        
        # Для целевой валюты
        elif event.widget == target_combobox:
            target_code = target_combobox.get()
            if target_code in cur:
                target_name = cur[target_code]
                target_label.config(text=f"Выбрано: {target_name}")
            else:
                target_label.config(text="")
                
    except Exception as e:
        print(f"Ошибка в update_c_label: {e}")


def get_exchange_rate():
    """Получение курса обмена валют"""
    base_code = base_combobox.get().strip()
    target_code = target_combobox.get().strip()
    
    # Проверка выбора валют
    if not base_code:
        mb.showwarning("Ошибка", "Выберите базовую валюту")
        return
    if not target_code:
        mb.showwarning("Ошибка", "Выберите целевую валюту")
        return
    if base_code == target_code:
        mb.showwarning("Ошибка", "Базовая и целевая валюта не могут быть одинаковыми")
        return
    
    try:
        # Получение данных от API
        response = requests.get(
            f"https://v6.exchangerate-api.com/v6/e48649bb9b00f650443eccb8/latest/{base_code}",
            timeout=10  # Добавляем таймаут
        )
        response.raise_for_status()
        data = response.json()
        
        # Проверка статуса API
        if data.get("result") != "success":
            mb.showerror("Ошибка", "Не удалось получить данные от сервера")
            return
            
        # Получение курса
        if target_code in data["conversion_rates"]:
            exchange_rate = data["conversion_rates"][target_code]
            base_name = cur[base_code]
            target_name = cur[target_code]
            
            # Форматирование сообщения
            message = f"1 {base_name} ({base_code}) = {exchange_rate:.4f} {target_name} ({target_code})"
            mb.showinfo("Курс обмена", message)
        else:
            mb.showerror("Ошибка", f"Валюта {target_code} не найдена в ответе API")
            
    except requests.exceptions.RequestException as e:
        mb.showerror("Ошибка сети", f"Проверьте подключение к интернету\n{str(e)}")
    except KeyError as e:
        mb.showerror("Ошибка данных", f"Неверный формат ответа от сервера")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла непредвиденная ошибка: {str(e)}")


# Словарь валют
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

# Создание главного окна
window = Tk()
window.title("Курсы обмена валют")
window.geometry("400x400")
window.resizable(False, False)

# Заголовок
Label(window, text="Конвертер валют", font=("Arial", 14, "bold")).pack(pady=10)

# Базовая валюта
Label(window, text="Базовая валюта", font=("Arial", 10)).pack(padx=10, pady=5)
base_combobox = ttk.Combobox(window, values=list(cur.keys()), width=35, state="readonly")
base_combobox.pack(padx=10, pady=5)
base_combobox.bind("<<ComboboxSelected>>", update_c_label)

base_label = ttk.Label(window, text="", font=("Arial", 9), foreground="blue")
base_label.pack(padx=10, pady=2)

# Целевая валюта
Label(window, text="Целевая валюта", font=("Arial", 10)).pack(padx=10, pady=10)
target_combobox = ttk.Combobox(window, values=list(cur.keys()), width=35, state="readonly")
target_combobox.pack(padx=10, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_c_label)

target_label = ttk.Label(window, text="", font=("Arial", 9), foreground="green")
target_label.pack(padx=10, pady=2)

# Кнопка получения курса
Button(window, text="Получить курс", command=get_exchange_rate, 
       bg="#4CAF50", fg="white", font=("Arial", 11), padx=20, pady=5).pack(pady=20)

# Информация о приложении
info_label = ttk.Label(window, text="Данные предоставлены ExchangeRate-API", 
                      font=("Arial", 8), foreground="gray")
info_label.pack(side=BOTTOM, pady=5)

window.mainloop()