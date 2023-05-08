import asyncio
import re
import time
from aiogram import Bot

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from core.logger import logger
from core.config import settings
from core.services import get_url_for_spy_proccess, update_price_for_url




async def spy_proccess(bot: Bot):
    logger.info("Start Spy Proccess...")
    while True:
        # (id, client_id, url, price)
        url_with_old_price = await get_url_for_spy_proccess()
        logger.debug(f"{url_with_old_price=}")
        # (url, price)
        url_with_new_price = await monitor_spy_seller_price(url_with_old_price)
        logger.debug(f"{url_with_new_price=}")
        for old, new in zip(url_with_old_price, url_with_new_price):
            if old[-1] != new[1]:
                await bot.send_message(chat_id=old[1], 
                                       text=f"🥷🏼 \nУ товара {old[2]} \nизменилась цена!\nСтарая цена: {old[-1]}\nНовая цена: {new[1]}")
                await update_price_for_url(settings.CLIENT_ID, url=old[2], new_price=new[1])
        logger.debug(f"Spy proccess sleep on {5 * 60} sec")
        await asyncio.sleep(5 * 60)


async def monitor_spy_seller_price(url_lst: list) -> list[tuple]:
    logger.info("monitor_spy_seller_price() ~ Start ")
    price_list = []
    service = Service(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    for url in url_lst:
        driver.get(url[2])
        logger.debug(f"monitor_spy_seller_price() ~ spying on {url[2]}")
        time.sleep(3)

        price_field = driver.find_element(
            By.CLASS_NAME, "price-block__final-price")
        logger.debug("monitor_spy_seller_price() ~ Price field found")
        price = int(re.sub(r'[^\d.]', '', price_field.text))
        price_list.append((url[2], price))
        logger.debug(
            f"monitor_spy_seller_price() ~ Price = {price}")

    driver.quit()
    logger.info("monitor_spy_seller_price() ~ Finish Selenium engine for spy")
    logger.debug(price_list)
    return price_list
    