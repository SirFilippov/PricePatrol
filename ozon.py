import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as BSoup

urls = [
    'https://www.ozon.ru/product/smartfon-poco-c51-2-64-gb-chernyy-1042982041/?avtc=1&avte=1&avts=1701066421',
    'https://www.ozon.ru/product/kishechnyy-fitosorbent-intestinal-defense-essential-sorbents-894038737/?avtc=1&avte=2&avts=1701066421',
    'https://www.ozon.ru/product/bolshaya-chashka-tsikoriy-s-ekstraktom-cherniki-85-g-580617195/?avtc=1&avte=2&avts=1701066421',
    'https://www.ozon.ru/product/planshet-argviu-planshet-14-pro-10-36-dyuyma-16-gb-ozu-1024-gb-pzu-russkiy-yazyk-1176040137/?avtc=1&avte=2&avts=1701066640',
    'https://www.ozon.ru/product/termobryuki-hosta-home-gornye-lyzhi-i-snoubord-759755421/?avtc=1&avte=2&avts=1701066640',
]


async def make_page_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            ignore_https_errors=True,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81')
        page = await context.new_page()
        await page.goto(url)
        page_content = await page.content()
        await browser.close()
        return page_content


def find_price(page_content: str = None):
    page_content = BSoup(page_content, 'lxml')
    try:
        price = page_content.find(class_='ol9 o7l').text
    except AttributeError:
        price = page_content.find(class_='p3l lp4 l8p').text

    return price


async def main():
    tasks = [make_page_content(url) for url in urls]
    page_contents = await asyncio.gather(*tasks)
    for index, page_content in enumerate(page_contents):
        try:
            find_price(page_content)
        except:
            with open(f'{index}test.html', 'w', encoding='utf-8') as out_html:
                out_html.write(page_content)


if __name__ == '__main__':
    asyncio.run(main())
