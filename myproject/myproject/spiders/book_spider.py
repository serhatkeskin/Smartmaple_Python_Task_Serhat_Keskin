import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from pymongo import MongoClient
import datetime



class KitapsepetiBookSpider(scrapy.Spider):
    name = 'kitapsepeti_book'
    main_site_url = 'https://www.kitapsepeti.com'
    collection_name = 'kitapsepeti'

    # MongoDB configuration
    mongo_uri = 'mongodb://localhost:27017/'
    database = 'smartmaple'
    
    def __init__(self, category_name="Roman", category_paramater="roman", isAvailable=1, starting_page=1, ending_page=None, *args, **kwargs):
        super(KitapsepetiBookSpider, self).__init__(*args, **kwargs)
        self.category_name = category_name
        self.category_paramater = category_paramater
        self.isAvailable = isAvailable
        self.starting_page = starting_page
        # print("###!!!type(self.starting_page)",type(self.starting_page))
        self.current_page = starting_page
        # print("###!!!type(self.current_page)",type(self.current_page))
        self.ending_page = ending_page
        self.start_urls = [f"https://www.kitapsepeti.com/{self.category_paramater}?stock={self.isAvailable}&pg={starting_page}"]
        self.rules = (
            Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
        )
        self.allowed_domains = ['kitapsepeti.com']
        self.custom_settings = {
            'ROBOTSTXT_OBEY': False,
        }

        #region logging and debugging
        print("\n### category: ",self.category_name)
        print("### category_paramater: ",self.category_paramater)
        print("### isAvailable: ",self.isAvailable)
        print("### start_urls: ",self.start_urls)
        print("### starting_page: ",self.starting_page)
        print("### ending_page: ",self.ending_page,"\n")
        #endregion

    def parse(self, response):
        print(f"\n### şuanki sayfa:({self.current_page}) kazılıyor... ###\n")

        for product in response.css('div.productItem'):
            try:
                price_element = response.css('div.currentPrice::text').get()
                cleaned_price = price_element.strip().replace('TL', '').replace(',', '.')
                numeric_price = float(cleaned_price)
                url=self.main_site_url+product.css('a.detailLink::attr(href)').get()

                data = {
                    'name': product.css('a.detailLink::attr(title)').get(),
                    'price': numeric_price,
                    'category_name': self.category_name,
                    'category_paramater': self.category_paramater,
                    'url': url,
                    'publisher': product.css('a.text-title.mt::text').get(),
                    'writer': product.css('a.text-title.fl::text').get(),
                    'datetime': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                }
                print("## product_data: ",data)

                # Save data to MongoDB
                self.save_to_mongodb(data, self.collection_name)

            except:
                print('Error while parsing price')
                pass

        print(f"\n### şuanki sayfa:({self.current_page}) başarıyla kazıldı. ###\n")
        next_page_num=int(self.current_page)+1
        next_page = response.css('a.next::attr(href)').get()

        # Write the current session info to a text file
        with open('last_session.txt', 'w') as f:
            session_info = f"{self.collection_name},{self.category_name},{self.category_paramater},{self.isAvailable},{next_page_num},{self.ending_page}"
            f.write(str(session_info))
            # print("###type(self.current_page)",type(self.current_page))
            # print("###type(self.starting_page)",type(self.starting_page))
            print(f"\n#### Sayfa {next_page_num} için şu anki session bilgisi last_session.txt dosyasına kaydedildi. ####\n")

        if next_page is not None and (self.ending_page is None or self.current_page < self.ending_page):
            self.current_page += 1
            yield response.follow(next_page, callback=self.parse)
    
    # Saving data to MongoDB database function
    def save_to_mongodb(self, data, collection_name):
        client = MongoClient(self.mongo_uri)
        db = client[self.database]
        collection = db[collection_name]
        collection.insert_one(data)
        client.close()


class KitapyurduBookSpider(scrapy.Spider):
    name = 'kitapyurdu_book'
    main_site_url = 'https://www.kitapyurdu.com'
    collection_name = 'kitapyurdu'

    # MongoDB configuration
    mongo_uri = 'mongodb://localhost:27017/'
    database = 'smartmaple'
    
    def __init__(self, category_name="Akademik", category_paramater="1033", isAvailable=1, starting_page=1, ending_page=None, *args, **kwargs):
        super(KitapyurduBookSpider, self).__init__(*args, **kwargs)
        self.category_name = category_name
        self.category_paramater = category_paramater
        self.isAvailable = isAvailable
        self.starting_page = starting_page
        self.current_page = starting_page
        self.ending_page = ending_page
        self.start_urls = [f"https://www.kitapyurdu.com/index.php?route=product/category&page={starting_page}&filter_category_all=true&path=1_{category_paramater}&filter_in_stock={isAvailable}&sort=purchased_365&order=DESC&limit=50"]
        self.rules = (
            Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
        )
        self.allowed_domains = ['kitapyurdu.com']
        self.custom_settings = {
            'ROBOTSTXT_OBEY': False,
        }

        #region logging and debugging
        print("\n### category: ",self.category_name)
        print("### category_paramater: ",self.category_paramater)
        print("### isAvailable: ",self.isAvailable)
        print("### start_urls: ",self.start_urls)
        print("### starting_page: ",self.starting_page)
        print("### ending_page: ",self.ending_page,"\n")
        #endregion

    def parse(self, response):
        print(f"\n### şuanki sayfa:({self.current_page}) kazılıyor... ###\n")

        for product in response.css('div.product-cr'):
            try:
                price_element = product.css('div.price div.price-new span.value::text').get()
                if not price_element: #kitapyurdunda bazı ürünler için fiyat tagi farklı olabiliyor
                    price_element = product.css('div.price span.price-old span.value::text').get()
                price_element= price_element.strip()
                # print("##price_element: ",price_element)
                cleaned_price = price_element.strip().replace(',', '.')
                # print("##cleaned_price: ",cleaned_price)
                numeric_price = float(cleaned_price)
                author = product.css('div.author a.alt span::text').get()
                author = author.strip() if author else None 

                data = {
                    'name': product.css('div.name a::attr(title)').get(),
                    'price': numeric_price,
                    'category_name': self.category_name,
                    'category_paramater': self.category_paramater,
                    'url': product.css('div.name a::attr(href)').get(),
                    'publisher': product.css('div.publisher a.alt span::text').get(),
                    'writer': author,
                    'datetime': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

                }
                print("## product_data: ",data)

                # Save data to MongoDB
                self.save_to_mongodb(data, self.collection_name)

            except:
                print('Error while parsing price')
                pass

        print(f"\n### şuanki sayfa:({self.current_page}) başarıyla kazıldı. ###\n")
        next_page_num=int(self.current_page)+1
        next_page = response.css('a.next::attr(href)').get()
        
        # Write the current session info to a text file
        with open('last_session.txt', 'w') as f:
            session_info = f"{self.collection_name},{self.category_name},{self.category_paramater},{self.isAvailable},{next_page_num},{self.ending_page}"
            f.write(str(session_info))
            # print("###type(self.current_page)",type(self.current_page))
            # print("###type(self.starting_page)",type(self.starting_page))
            print(f"\n#### Sayfa {next_page_num} için şu anki session bilgisi last_session.txt dosyasına kaydedildi. ####\n")


        if next_page is not None and (self.ending_page is None or self.current_page < self.ending_page):
            self.current_page += 1
            yield response.follow(next_page, callback=self.parse)
    
    # Saving data to MongoDB database function
    def save_to_mongodb(self, data, collection_name):
        client = MongoClient(self.mongo_uri)
        db = client[self.database]
        collection = db[collection_name]
        collection.insert_one(data)
        client.close()