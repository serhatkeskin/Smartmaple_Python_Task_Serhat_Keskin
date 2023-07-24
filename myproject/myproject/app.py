from scrapy.crawler import CrawlerProcess
import sys
# Import your spider class
from spiders.book_spider import KitapsepetiBookSpider, KitapyurduBookSpider


def run_book_spider(BookSpider_Cls, category_name, category_paramater, isAvailable, starting_page=1, ending_page=None):
    # Create a CrawlerProcess with custom settings
    process = CrawlerProcess(settings={
        # 'FEED_FORMAT': 'json',   # Specify the export format as JSON
        # 'FEED_URI': f'kitapsepeti-{category}-books.json',  # Specify the output file path if you want to export JSON file
        'FEED_EXPORT_ENCODING': 'utf-8',  # Set the encoding for the JSON file
        # 'FEED_EXPORT_INDENT': None,  # Generate JSON objects without indentation
    })

    # Add your spider to the process
    process.crawl(BookSpider_Cls, category_name=category_name, category_paramater=category_paramater, isAvailable=isAvailable, starting_page=starting_page, ending_page=ending_page)

    # Start the crawling process
    process.start()

##############################################################################################################

if __name__ == "__main__":
    if len(sys.argv) != 7: # script adı dahil 7 argüman bekleniyor
        if len(sys.argv) == 1: # script adı dahil 1 argüman varsa kullanıcıdan inputlar alınarak argümanlar toplanıyor
            pass
        else:
            print("Kullanım: python app.py <site> <kategori> <kategori_url_parametresi> <satışta olma durumu> <başlangıç sayfası> <bitiş sayfası>"
                  "\nVeya hiç argüman girmeden çalıştırın: python app.py ")
            sys.exit(1)

    if len(sys.argv) == 7:
        schedule_flag = True

        site = sys.argv[1]
        print("site: ", site)
        category_name = sys.argv[2]
        print("category_name: ", category_name)
        category_paramater = sys.argv[3]
        print("category_paramater: ", category_paramater)
        isAvailable = int(sys.argv[4])
        print("isAvailable: ", isAvailable)
        starting_page = int(sys.argv[5])
        print("starting_page: ", starting_page)
        ending_page = int(sys.argv[6])
        print("ending_page: ", ending_page)

        if site=="kitapyurdu":
            run_book_spider(BookSpider_Cls=KitapyurduBookSpider,category_name=category_name, category_paramater=category_paramater, isAvailable=isAvailable, starting_page=starting_page, ending_page=ending_page)
            print("Kitapyurdu kitap bilgilerini kazıma işlemi tamam, Çıkış yapıldı!")
            exit()
        elif site=="kitapsepeti":
            run_book_spider(BookSpider_Cls=KitapsepetiBookSpider,category_name=category_name, category_paramater=category_paramater, isAvailable=isAvailable, starting_page=starting_page, ending_page=ending_page)
            print("Kitapsepeti kitap bilgilerini kazıma işlemi tamam, Çıkış yapıldı!")
            exit()
        else:
            print("Hatalı site seçimi. Çıkış yapılıyor.")
            exit()


    
    # region INPUT 0 - Create New Session or Continue Last session
    last_session = input("Son kazıma işleminin kaldığı yerden devam etmek için '1' yazınız. Yeni kazıma işlemi için boş bırakınız. Çıkmak için 'exit' yazınız: \n")
    if last_session.lower() == "exit":
        print("Çıkış yapılıyor.")
        exit()
    elif last_session == "1":
        with open('last_session.txt', 'r') as f:
            session_info = f.read()
            session_info = session_info.split(",")
            print(session_info)
            chosen_site = session_info[0]
            selected_category_name = session_info[1]
            selected_category_parameter = session_info[2]
            isAvailable = int(session_info[3])
            starting_page = int(session_info[4])
            ending_page = int(session_info[5])
            print("Last session info: ", session_info)
            if chosen_site == "kitapyurdu":
                run_book_spider(BookSpider_Cls=KitapyurduBookSpider,category_name=selected_category_name, category_paramater=selected_category_parameter, isAvailable=isAvailable, starting_page=starting_page, ending_page=ending_page)
                print("Kitapyurdu kitap bilgilerini kazıma işlemi tamam, Çıkış yapıldı!")
            elif chosen_site == "kitapsepeti":
                run_book_spider(BookSpider_Cls=KitapsepetiBookSpider,category_name=selected_category_name, category_paramater=selected_category_parameter, isAvailable=isAvailable, starting_page=starting_page, ending_page=ending_page)
                print("Kitapsepeti kitap bilgilerini kazıma işlemi tamam, Çıkış yapıldı!")
            exit()
    elif last_session == "":
        pass
    else:
        print("Hatalı giriş. Çıkış yapılıyor.")
        exit()
    # endregion

    # region INPUT 1 - Site seçimi
    chosen_site=input("kitap yurdu için 1, kitap sepeti için 2 giriniz. Çıkmak için bu değerlerden farklı bir değer giriniz veya 'exit' yazınız: \n")
    if chosen_site.lower()=="exit":
        print("Çıkış yapılıyor.")
        exit()
    elif chosen_site=="1":
        url="https://www.kitapyurdu.com/cizgi-roman?stock=1"
        site="kitapyurdu"
    elif chosen_site=="2":
        url="https://www.kitapsepeti.com/cizgi-roman?stock=1"
        site="kitapsepeti"
    else:
        print("Çıkış yapılıyor.")
        exit()
    # endregion

    # region INPUT 2 - Kategori seçimi
    if chosen_site == "1":
        # url = "https://www.kitapyurdu.com/cizgi-roman?stock=1"
        site = "kitapyurdu"
        categories={ # kitapyurdu.com'daki kategori isimleri ve url parametreleri
        "Akademik": "1033",
        "Edebiyat": "128",
        "Psikoloji": "87",
        "Sanat": "172",
        "Tarih": "41",
        "Kişisel Gelişim": "341",
        "Çocuk Kitapları": "2",
        }
        print("İstediğiniz kategorinin numarasını yazınız")
        for num, category_name in enumerate(categories, start=1):
            print(f"{num}. {category_name}")
    elif chosen_site == "2":
        # url = "https://www.kitapsepeti.com/cizgi-roman?stock=1"
        site = "kitapsepeti"
        categories={ # kitapsepeti.com'daki kategori isimleri ve url parametreleri
        "Roman": "roman",
        "Çizgi Roman": "cizgi-roman",
        "Çocuk Kitapları": "cocuk-kitaplari",
        "Sınav Kitapları": "sinavlara-hazirlik-kitaplari",
        "Bilim Kurgu": "bilimkurgu",
        "Türk Edebiyatı": "turk-edebiyati",
        "Çok Satanlar": "cok-satan-kitaplar",
        }
        print("İstediğiniz kategorinin numarasını yazınız")
        for num, category_name in enumerate(categories, start=1):
            print(f"{num}. {category_name}")
    else:
        print("Yanlış girildi. Çıkış yapılıyor.")
        exit()

    selected_number = input("Lütfen kategori numarasını seçiniz. Çıkmak için 'exit' yazınız: \n")
    if selected_number.lower() == "exit":
        print("Çıkış yapılıyor.")
        exit()
    # Check if the chosen number is valid
    try:
        selected_number = int(selected_number)
        if selected_number not in range(1, len(categories) + 1):
            raise ValueError
    except ValueError:
        print("Geçersiz kategori numarası. Çıkış yapılıyor.")
        exit()

    selected_category_name = list(categories.keys())[selected_number - 1]
    # print(f"Seçilen kategori: {selected_category_name}")
    selected_category_parameter = list(categories.values())[selected_number - 1]
    # print(f"Seçilen kategori parametresi: {selected_category_parameter}")
    # endregion

    # region INPUT 3 - Stok durumu
    isAvailable = input("Satışta olanlar için 1, tüm ürünler için 2 giriniz. Çıkmak için bu değerlerden farklı bir değer giriniz veya 'exit' yazınız: \n")
    if isAvailable.lower() == "exit":
        print("Çıkış yapılıyor.")
        exit()
    elif isAvailable=="1":
        isAvailable=1
    elif isAvailable=="2":
        isAvailable=0
    else:
        print("Çıkış yapılıyor.")
        exit()
    # endregion

    # region INPUT 4 - Kaçıncı sayfadan başlanacağı
    starting_page = input("Kaçıncı sayfadan başlamak istiyorsunuz. 1.sayfadan başlamak için boş bırakınız. Çıkmak için 'exit' yazınız: \n")
    if starting_page.lower() == "exit":
        print("Çıkış yapılıyor.")
        exit()
    elif starting_page == "":
        starting_page = 1
    else:
        try:
            starting_page = int(starting_page)
            if starting_page < 1:
                print("Hatalı giriş: Sayfa sayısı 1'den küçük olamaz.")
                exit()
        except ValueError:
            print("Hatalı giriş: Geçersiz sayı formatı.")
            exit()
    # endregion

    # region INPUT 5 - Maksimum kaçıncı sayfaya kadar kazım yapılacağı
    ending_page = input("Maksimum kaçıncı sayfaya kadar kazmak istiyorsunuz. Geriye kalan bütün sayfalar için boş bırakınız. Çıkmak için 'exit' yazınız: \n")
    if ending_page.lower() == "exit":
        print("Çıkış yapılıyor.")
        exit()
    elif ending_page == "":
        ending_page = None
    else:
        try:
            ending_page = int(ending_page)
            if ending_page < 1:
                print("Hatalı giriş: Maksimum sayfa sayısı 1'den küçük olamaz.")
                exit()
            if ending_page < starting_page:
                print("Hatalı giriş: Maksimum sayfa sayısı başlangıç sayfasından küçük olamaz.")
                exit()
        except ValueError:
            print("Hatalı giriş: Geçersiz sayı formatı.")
            exit()
    # endregion

    
    if site=="kitapyurdu":
        run_book_spider(BookSpider_Cls=KitapyurduBookSpider,category_name=selected_category_name, category_paramater=selected_category_parameter, isAvailable=isAvailable, starting_page=starting_page, ending_page=ending_page)
        print("Kitapyurdu kitap bilgilerini kazıma işlemi tamam, Çıkış yapıldı!")
    elif site=="kitapsepeti":
        run_book_spider(BookSpider_Cls=KitapsepetiBookSpider,category_name=selected_category_name, category_paramater=selected_category_parameter, isAvailable=isAvailable, starting_page=starting_page, ending_page=ending_page)
        print("Kitapsepeti kitap bilgilerini kazıma işlemi tamam, Çıkış yapıldı!")
    else:
        print("Hatalı site seçimi. Çıkış yapılıyor.")
        exit()
