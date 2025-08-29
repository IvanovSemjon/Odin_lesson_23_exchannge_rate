import asyncio
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import io
import requests
from g4f.client import AsyncClient
import threading

class ImageGeneratorApp:
    def __init__(self, root):
        """
        Инициализация главного окна приложения
        root: главное окно Tkinter
        """
        self.root = root
        self.root.title("Генератор изображений")
        self.root.geometry("800x600")
        
        # Создаем виджет Notebook (вкладки) для отображения нескольких изображений
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем главную вкладку с элементами управления
        self.create_main_tab()
        
        # Инициализируем асинхронного клиента для генерации изображений
        self.client = AsyncClient()
        
        # Создаем отдельный event loop для asyncio
        self.loop = asyncio.new_event_loop()
        
        # Флаг для отслеживания работы приложения
        self.running = True
        
    def create_main_tab(self):
        """
        Создает главную вкладку с элементами управления
        """
        main_tab = ttk.Frame(self.notebook)
        self.notebook.add(main_tab, text="Управление")
        
        # Поле для ввода промпта
        tk.Label(main_tab, text="Введите описание изображения:").pack(pady=5)
        self.prompt_entry = tk.Entry(main_tab, width=50)
        self.prompt_entry.pack(pady=5, padx=10)
        self.prompt_entry.bind('<Return>', lambda e: self.generate_image())
        
        # Кнопка генерации
        generate_btn = tk.Button(main_tab, text="Сгенерировать изображение", 
                               command=self.generate_image)
        generate_btn.pack(pady=10)
        
        # Область для вывода статуса
        self.status_text = scrolledtext.ScrolledText(main_tab, height=10, width=70)
        self.status_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.status_text.config(state=tk.DISABLED)
        
    def log_status(self, message):
        """
        Добавляет сообщение в лог статуса (вызывается из главного потока)
        """
        # Проверяем, не закрыто ли окно
        if not self.running:
            return
            
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        
    def generate_image(self):
        """
        Запускает процесс генерации изображения в отдельном потоке
        """
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            messagebox.showwarning("Предупреждение", "Введите описание изображения!")
            return
            
        self.log_status(f"Начата генерация: {prompt}")
        
        # Запускаем генерацию в отдельном потоке
        thread = threading.Thread(target=self.run_async_task, args=(prompt,))
        thread.daemon = True
        thread.start()
        
    def run_async_task(self, prompt):
        """
        Запускает асинхронную задачу в отдельном event loop
        """
        # Устанавливаем новый event loop для этого потока
        asyncio.set_event_loop(self.loop)
        
        # Запускаем асинхронную задачу
        try:
            self.loop.run_until_complete(self.async_generate_image(prompt))
        except Exception as e:
            # Обрабатываем ошибки и обновляем UI через главный поток
            self.root.after(0, lambda: self.log_status(f"Ошибка: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
        
    async def async_generate_image(self, prompt):
        """
        Асинхронно генерирует изображение по промпту
        """
        try:
            # Обновляем статус через главный поток
            self.root.after(0, lambda: self.log_status(f"Генерация изображения: {prompt}..."))
            
            # Генерируем изображение
            response = await self.client.images.generate(
                prompt=prompt,
                model="flux",
                response_format="url"
            )
            
            image_url = response.data[0].url
            self.root.after(0, lambda: self.log_status(f"Изображение сгенерировано! URL: {image_url}"))
            
            # Загружаем и отображаем изображение
            await self.display_image(prompt, image_url)
            
            self.root.after(0, lambda: self.log_status("Готово!"))
            
        except Exception as e:
            # Обрабатываем ошибки через главный поток
            self.root.after(0, lambda: self.log_status(f"Ошибка: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
    
    async def display_image(self, prompt, image_url):
        """
        Загружает изображение по URL и отображает его
        """
        try:
            self.root.after(0, lambda: self.log_status("Загрузка изображения..."))
            
            # Загружаем изображение
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Создаем изображение PIL
            image_data = io.BytesIO(response.content)
            pil_image = Image.open(image_data)
            
            # Масштабируем для отображения
            max_size = (400, 400)
            pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Создаем вкладку через главный поток
            self.root.after(0, lambda: self.create_image_tab(prompt, pil_image))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_status(f"Ошибка загрузки: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}"))
    
    def create_image_tab(self, prompt, pil_image):
        """
        Создает вкладку с изображением (вызывается из главного потока)
        """
        # Создаем новую вкладку
        image_tab = ttk.Frame(self.notebook)
        
        # Конвертируем PIL image в PhotoImage
        photo_image = ImageTk.PhotoImage(pil_image)
        
        # Создаем метку для изображения
        image_label = tk.Label(image_tab, image=photo_image)
        image_label.image = photo_image  # Сохраняем ссылку
        image_label.pack(pady=10)
        
        # Добавляем подпись
        caption_label = tk.Label(image_tab, text=f"Запрос: {prompt}", wraplength=300)
        caption_label.pack(pady=5)
        
        # Добавляем вкладку в notebook
        tab_text = prompt[:20] + "..." if len(prompt) > 20 else prompt
        self.notebook.add(image_tab, text=tab_text)
        self.notebook.select(image_tab)  # Переключаемся на новую вкладку
    
    def on_closing(self):
        """
        Обработчик закрытия окна
        """
        self.running = False
        self.loop.stop()
        self.root.destroy()

def main():
    """
    Главная функция приложения
    """
    root = tk.Tk()
    app = ImageGeneratorApp(root)
    
    # Устанавливаем обработчик закрытия окна
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    try:
        # Запускаем главный цикл Tkinter
        root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()

if __name__ == "__main__":
    main()