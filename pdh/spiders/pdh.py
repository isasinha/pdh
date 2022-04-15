import scrapy
 
class PdhSpider(scrapy.Spider):
    name = 'PdH'
    allowed_domains = ['papodehomem.com.br']
    start_urls = ['https://papodehomem.com.br/colecoes/melhor-do-pdh']

    def parse(self, response):
        for papo in response.css("ol.articles").css("h2 a::attr(href)").getall():
            text_page = f"https://papodehomem.com.br{papo}"
            yield scrapy.Request(text_page, callback=self.parse_text)
        pass
        proxima_pagina = response.css('a.nocache::attr(href)').get()
        link_proxima_pagina = f"{proxima_pagina}"
        if link_proxima_pagina is not None:
            link_proxima_pagina = response.urljoin(link_proxima_pagina)
            yield scrapy.Request(link_proxima_pagina, callback=self.parse) 
    
    def parse_text(self, response):
        content = ""   

        title = response.css('header.entry-header h1::text').get()
        subtitle = response.css('header.entry-header p::text').get()

        for line in response.css('article.entry-content p::text').getall() :
            content = content + "".join(line) + "\n"            

        post = {                      
            'title': title, #.encode('utf-8'),
            'subtitle': subtitle, #.encode('utf-8'),
            'content': content #.encode('utf-8')
        }     

        yield post