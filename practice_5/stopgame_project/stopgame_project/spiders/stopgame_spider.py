## Создание паучка, сбор данных и сохранение их в бд

import pandas as pd
from pymongo import MongoClient
import scrapy
import hashlib
from urllib.parse import urljoin
import pandas as pd


class StopgameBlogsSpider(scrapy.Spider):
    name = 'game_blogs'
    allowed_domains = ['stopgame.ru']
    start_urls = ['https://stopgame.ru/blogs/all1']
    
    def __init__(self, *args, **kwargs):
        super(StopgameBlogsSpider, self).__init__(*args, **kwargs)
        self.games_blogs_data = []
    
    def parse(self, response):
        # Парсинг блогов с XPath
        blog_cards = response.xpath('//article[contains(@class, "_card_1lcny_4")]')
        
        for card in blog_cards:
            try:
                # Название блога
                title_elem = card.xpath('.//a[contains(@class, "_title_1lcny_24")]')
                title = title_elem.xpath('string()').get().strip() if title_elem else "No title"
                
                # Ссылка на блог
                link = card.xpath('.//a[contains(@class, "_title_1lcny_24")]/@href').get()
                link = urljoin("https://stopgame.ru", link) if link else "No link"
                
                # Автор
                author = card.xpath('.//span[@class="_user-info__name_g4zbt_1176"]/text()').get()
                author = author.strip() if author else "Unknown"
                
                # Ссылка на страницу автора
                author_link = card.xpath('.//a[contains(@class, "_user-info_g4zbt_1124")]/@href').get()
                author_link = urljoin("https://stopgame.ru", author_link) if author_link else "No author link"
                
                # Дата публикации
                date = card.xpath('.//section[contains(@class, "_date_1lcny_225")]//text()').get()
                date = date.strip() if date else "No date"
                
                # Рейтинг
                rating = card.xpath('.//div[contains(@class, "_rating_1lcny_92")]//text()').get()
                rating = rating.strip() if rating else "0"
                
                # Количество комментариев
                comments_elem = card.xpath('.//a[contains(@class, "_info__attribute_1lcny_241")][last()]//text()')
                comments = comments_elem.get().strip().split()[0] if comments_elem else "0"
                
                # Тип контента (Блог, Обзоры и рассуждения)
                content_type = card.xpath('.//section[contains(@class, "_section_1lcny_122")]/span//text()').get()
                content_type = content_type.strip() if content_type else "Блог"
                
                # Генерация уникального data_key на основе ссылки
                if link != "No link":
                    data_key = hashlib.md5(link.encode()).hexdigest()
                else:
                    data_key = hashlib.md5(f"{title}_{author}_{date}".encode()).hexdigest()
                
                blog_item = {
                    'title': title,
                    'author': author,
                    'date': date,
                    'rating': rating,
                    'comments': comments,
                    'content_type': content_type,
                    'link': link,
                    'data_key': data_key
                }
                
                self.games_blogs_data.append(blog_item)
                yield blog_item
                
            except Exception as e:
                self.logger.error(f"Error parsing card: {e}")
                continue
    
    def closed(self, reason):
        # Создание DataFrame после завершения парсинга
        if self.games_blogs_data:
            df = pd.DataFrame(self.games_blogs_data)
            print(f"Найдено блогов: {len(df)}")
            print("\nПервые 5 записей:")
            print(df.head())
            
            # Сохранение в CSV
            df.to_csv('stopgame_blogs.csv', index=False, encoding='utf-8')
            print("Данные сохранены в stopgame_blogs.csv")
        else:
            print("Не найдено данных для сохранения")