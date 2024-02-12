import asyncio
import aiohttp
import sys
from datetime import datetime, timedelta


async def fetch_currency(session, date):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime("%d.%m.%Y")}'
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            currency_data = {'EUR': {}, 'USD': {}}
            for exchange in data['exchangeRate']:
                if exchange.get('currency') == 'EUR':
                    currency_data['EUR']['sale'] = exchange.get('saleRate', 'Not available')
                    currency_data['EUR']['purchase'] = exchange.get('purchaseRate', 'Not available')
                elif exchange.get('currency') == 'USD':
                    currency_data['USD']['sale'] = exchange.get('saleRate', 'Not available')
                    currency_data['USD']['purchase'] = exchange.get('purchaseRate', 'Not available')

            return {date.strftime('%Y-%m-%d'): currency_data}
        else:
            print(f"Помилка отримання даних за {date.strftime('%d.%m.%Y')}: Статус {response.status}")
            return None


async def main(days):
    if days < 1 or days > 10:
        print("Кількість днів повинна бути між 1 та 10")
        return

    async with aiohttp.ClientSession() as session:
        tasks = []
        for day in range(days):
            date = datetime.now() - timedelta(days=day)
            tasks.append(fetch_currency(session, date))
        results = await asyncio.gather(*tasks)
        print([result for result in results if result is not None])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Запуск програми: py main.py <к-сть днів>")
    else:
        try:
            days = int(sys.argv[1])
            asyncio.run(main(days))
        except ValueError:
            print('Кількість днів повинна бути цілим числом')