import scrapy

class BooksDetails(scrapy.Spider):
    count = 1  
    name = "bookdetail"
    max_count = 4000  

    def start_requests(self):
        
        url = f"https://fidibo.com/book/{self.count}"
        yield scrapy.Request(url=url, callback=self.parse, errback=self.errback_httpbin)

    def parse(self, response):
        
        title = response.css("div.book-buy-box-detail-content-title::text").get()
        auther = response.css("div.book-author-detail div::text").get()
        publisher = response.css("div.book-buy-box-detail-content-publisher::text").get()
        rating = response.css("div.book-buy-box-header-rate-title::text").get()
        category = response.css("div.book-introduction-categories-items a::text").get()
        image = response.css("div.book-main-box img::attr(src)").get()


        if title:
            
            yield {
                "Title": title,
                "Auther": auther,
                "Publisher": publisher,
                "Rating": rating,
                "Category": category,
                "Image": image
            }
        else:
            
            self.logger.warning(f"No valid content found for URL: {response.url}")

        self.count += 1

        if self.count <= self.max_count:
            next_url = f"https://fidibo.com/book/{self.count}"
            
            yield scrapy.Request(url=next_url, callback=self.parse, errback=self.errback_httpbin)

    def errback_httpbin(self, failure):
        
        self.logger.error(repr(failure))

        if failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            response = failure.value.response
            if response.status == 404:
                self.logger.warning(f"Page not found (404): {response.url}")
            else:
                self.logger.error(f"Unhandled HTTP error: {response.status} on {response.url}")

        self.count += 1

        if self.count <= self.max_count:
            next_url = f"https://fidibo.com/book/{self.count}"
            
            yield scrapy.Request(url=next_url, callback=self.parse, errback=self.errback_httpbin)
