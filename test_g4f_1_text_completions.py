import asyncio
import sys
from g4f.client import AsyncClient

# Настройка кодировки для корректного отображения русского текста
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    try:
        client = AsyncClient()
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Скажи какое сегодня число, посмотри в интернете"
                }
            ],
            web_search=True
        )
        
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())