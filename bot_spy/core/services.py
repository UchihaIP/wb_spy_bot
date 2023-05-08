import sqlite3

from core.logger import logger


class MemoryDB:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS urls(id integer PRIMARY KEY, client_id INTEGER, url TEXT, price INTEGER);')

    async def add_one_url(self, client_id: int, url: str) -> None:
        self.cursor.execute('INSERT INTO urls VALUES (?, ?, NULL);', (client_id, url))
        self.conn.commit()

    async def add_many_urls(self, client_id: int, urls: list[str]) -> None:
        values = [(client_id, url.strip("\n")) for url in urls]
        self.cursor.executemany('INSERT INTO urls(client_id, url, price) VALUES (?, ?, NULL);', values)
        self.conn.commit()

    async def delete_url(self, client_id: int, index: int) -> None:
        self.cursor.execute('DELETE FROM urls WHERE client_id = ? AND id = ?;', (client_id, index))
        self.conn.commit()

    async def get_url_ids(self, client_id: int) -> list[int]:
        self.cursor.execute('SELECT id FROM urls WHERE client_id = ?;', (client_id,))
        urls = [row[0] for row in self.cursor.fetchall()]
        logger.debug(f"get_url_ids() -> {urls}")
        return urls if urls else None

    async def get_url_and_price(self, client_id: int) -> list[tuple]:
        self.cursor.execute('SELECT id, url, price FROM urls WHERE client_id = ?;', (client_id,))
        result = self.cursor.fetchall()
        export_list = []
        for row in result:
            export_list.append(row)
        print(export_list)
        return export_list

    async def update_price_for_url(self, client_id: int, url: str, price: int):
        self.cursor.execute('UPDATE urls SET price = ? WHERE client_id = ? AND url = ?;', (price, client_id, url))
        self.conn.commit()


db = MemoryDB("wb_spy.db")

async def get_spy_list(client_id: int):
    urls_with_price = await db.get_url_and_price(client_id)
    if urls_with_price:
        text = "🥷🏼 Список отслеживаемых ссылок. \n\n"
        for url in urls_with_price:
            text += f"{url[0]}. {url[1]} \nТекущая цена: {url[2]}\n\n"
        return text, True
    return "🥷🏼 Ты ещё не вносил ссылки для отслеживания.", None


async def get_lenght_spy_list(client_id: int):
    urls = await db.get_url_ids(client_id)
    if urls:
        return urls
    return None

async def add_urls_in_db(client_id: int, urls: list[str]) -> bool:
    lenght_urls_list = len(urls)
    if lenght_urls_list > 1:
        await db.add_many_urls(client_id, urls=urls)
        return True
    elif lenght_urls_list == 1:
        await db.add_one_url(client_id, urls[0])
        return True
    else:
        return False

async def delete_url(client_id: int, index: int):
    await db.delete_url(client_id, index)


async def get_url_for_spy_proccess(client_id: int):
    return await db.get_url_and_price(client_id)


async def update_price_for_url(client_id: int, url: str, new_price: int):
    return await db.update_price_for_url(client_id=client_id, url=url, price=new_price)
