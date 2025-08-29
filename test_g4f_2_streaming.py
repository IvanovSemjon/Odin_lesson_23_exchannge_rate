import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()

    stream = client.chat.completions.stream(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "role": "system", "content": "Ты преподаватель в школе для 5 классов",
                "content": "Напиши Что такое библиотека g4f"
            }
        ],
        web_search = True
    )

    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")

asyncio.run(main())