import time

import aiohttp
import asyncio

import re

data = [
    'https://www.wildberries.ru/catalog/140102726/detail.aspx',
    'https://www.wildberries.ru/catalog/141609063/detail.aspx',
    'https://www.wildberries.ru/catalog/176482242/detail.aspx',
    'https://www.wildberries.ru/catalog/176666624/detail.aspx',
    'https://www.wildberries.ru/catalog/135856538/detail.aspx',
    'https://www.wildberries.ru/catalog/131758770/detail.aspx',
    'https://www.wildberries.ru/catalog/76804208/detail.aspx',
    'https://www.wildberries.ru/catalog/110245376/detail.aspx',
    'https://www.wildberries.ru/catalog/3627670/detail.aspx',
    'https://www.wildberries.ru/catalog/178646785/detail.aspx',
    'https://www.wildberries.ru/catalog/174942583/detail.aspx',
    'https://www.wildberries.ru/catalog/149773293/detail.aspx',
    'https://www.wildberries.ru/catalog/101646321/detail.aspx',
    'https://www.wildberries.ru/catalog/152003278/detail.aspx',
    'https://www.wildberries.ru/catalog/99623079/detail.aspx',
    'https://www.wildberries.ru/catalog/150327369/detail.aspx',
]


async def api_maker(items_urls):
    async with aiohttp.ClientSession(trust_env=True) as session:
        for item_url in items_urls:
            item_id = re.search(r'\d+', item_url).group()
            part = item_id[:-3]
            vol = part[:-2]
            for basket_num in range(1, 13):
                basket_num = str(basket_num).rjust(2, '0')
                potential_api = f'https://basket-{basket_num}.wb.ru/vol{vol}/part{part}/{item_id}/info/ru/card.json'
                async with session.get(potential_api) as response:
                    if response.status == 200:
                        print(potential_api)
                        break


async def price_getter(items_urls):
    async with aiohttp.ClientSession(trust_env=True) as session:
        for item_url in items_urls:
            item_id = re.search(r'\d+', item_url).group()
            main_api = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=123585937&spp=25&nm={item_id}'
            async with session.get(main_api) as response:
                res = await response.json()
                for product in res['data']['products']:
                    if str(product['id']) == item_id:
                        print(item_url)
                        print(str(product['salePriceU'])[:-2] + 'р.')

# https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=123585937&spp=25&nm=174942583
# "nm_id": 174942583,

if __name__ == '__main__':
    start_time = time.time()
    # asyncio.run(api_maker(data))
    asyncio.run(price_getter(data))
    end_time = time.time()
    print(end_time - start_time)