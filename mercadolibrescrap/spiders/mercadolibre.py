# Primero, importamos los módulos necesarios de Scrapy.
import scrapy
import os
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

# Elimina el archivo data.json
if os.path.exists("data.json"):
    os.remove("data.json")

# Definimos un item de Scrapy para los datos que queremos extraer.
class Book(Item):
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    sales = scrapy.Field(output_processor=TakeFirst())
    approximate_sales = scrapy.Field(output_processor=TakeFirst())
    image = scrapy.Field(output_processor=TakeFirst())

# Definimos la spider de Scrapy.
class MercadolibreSpider(scrapy.Spider):
    name = "mercadolibre"
    
    # Definimos algunos ajustes personalizados para la spider.
    # Establecemos el agente de usuario y limitamos el número de páginas a recorrer.
    custom_settings = {
        'USER_AGENT': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'CLOSESPIDER_PAGECOUNT': 20
    }
    
    allowed_domains = ["www.mercadolibre.com.ve", "articulo.mercadolibre.com.ve", "listado.mercadolibre.com.ve"]
    
    start_urls = ["https://listado.mercadolibre.com.ve/"]
    
    # Definimos el método de parseo.    
    def parse(self, response):
        
        # Definimos las palabras clave para las que queremos buscar.
        keywords = ['libros','cpu','perros','tarjeta','peluches']
        
        # Para cada palabra clave, generamos una URL y hacemos una petición a esa URL.
        for keyword in keywords:
            print(keyword)
            yield response.follow(f'https://listado.mercadolibre.com.ve/{keyword}#D[A:{keyword}]', callback=self.listB)

    # Este método se llama para cada respuesta de las URLs de las palabras clave.
    # Extrae el enlace de detalle del primer producto y hace una petición a esa URL.
    def listB(self, response):
        linkDetails = response.xpath('//div/div[2]/section/ol/li[1]/div/div/div[2]/div[1]/a/@href').get()
        # Existen dos vistas de los articulos, si no funciona la primera, se prueba la segunda
        if(linkDetails):
            yield response.follow(linkDetails, callback=self.details)
        else:
            linkDetails = response.xpath('/html/body/main/div/div[2]/section/ol/div[1]/li[1]/div/div/div[2]/div/div[1]/a/@href').get()
            yield response.follow(linkDetails, callback=self.details)
            
    # Este método se llama para cada respuesta de las URLs de los detalles del producto.
    # Extrae los datos del producto y los carga en un item.        
    def details(self, response):
        
        # Extrae el precio  exacto del producto.
        priceInt = (response.xpath('//div/div[1]/div[1]/div/div/span/span/span[2]/text()').get()).replace(".","")
        priceDec = response.xpath('//div/div[1]/div[1]/div/div/span/span/span[4]/text()').get()
        price = int(priceInt)
        print(price)
        
        # Extrae la cantidad de ventas del producto en numero.
        sales = response.xpath('//div[5]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/span/text()').get()
        sales_words = sales.split(" ")
        sale_int = sales_words[4]
        print(sale_int)
        
        if (len(sale_int) > 1):
            sales_approx = int(sale_int[1])
        else:
            sales_approx = int(sale_int)    
        
        
        if( str(priceDec) != 'None' ):
            price = float(str(priceInt) + '.' + str(priceDec))
            
            
        # Carga los datos en el item.
        item = ItemLoader(Book(), response)
        
        item.add_xpath('title', '//div[2]/div[5]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/h1/text()')
        item.add_value('price', price)
        item.add_xpath('sales', '//div[5]/div/div[1]/div/div[1]/div/div[1]/div/div[1]/span/text()')
        item.add_value('approximate_sales', sales_approx) 
        item.add_xpath('image', '//div[1]/div/div/div/div/span/figure/img/@src')
        
        # Devuelve el item.
        yield item.load_item()
            
    

   
        
