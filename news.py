import asyncio

import feedparser
import requests

from bot_instance import bot

chat_id = '2119353166'
sent_links = set()
RSS_FEED_URL = "https://www.sports.ru/rss/main.xml"

def test_news():
    feed = feedparser.parse(RSS_FEED_URL)
    print(feed.entries[:5])  # Вывод первых 5 записей
async def test_bot():
    try:
        await bot.send_message(chat_id=2119353166, text="Тестовое сообщение", parse_mode="HTML")
        print("Сообщение отправлено успешно!")
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
def get_latest_news():
    try:
        feed = feedparser.parse(RSS_FEED_URL)
        news = []
        for entry in feed.entries:
            if entry.link not in sent_links:
                sent_links.add(entry.link)
                news.append(f"📰 <b>{entry.title}</b>n{entry.link}")
        return news
    except Exception as e:
        print(f"Ошибка при парсинге RSS: {e}")
        return []

# Фоновая задача для отправки новостей
async def news_task():
    while True:
        news = get_latest_news()
        for item in news:
            try:
                await bot.send_message(chat_id=chat_id, text=item, parse_mode="HTML")
            except Exception as e:
                print(f"Ошибка отправки сообщения: {e}")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(news_task())