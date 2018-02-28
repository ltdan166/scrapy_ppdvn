# -*- coding: utf-8 -*-
import scrapy


class PpdvnpubSpider(scrapy.Spider):
    name = 'ppdvnpub'
    allowed_domains = ['ppdvn.gov.vn']
    start_urls = ['https://ppdvn.gov.vn/web/guest/ke-hoach-xuat-ban?query=&id_nxb=1']
    for i in range (2, 68):
        url = 'https://ppdvn.gov.vn/web/guest/ke-hoach-xuat-ban?query=&id_nxb='+str(i)
        start_urls.append (url)


    def parse(self, response):
        #header information
        #hdrinf = dict ()
        #hdrinf['Seq'] = response.xpath ('//*[@id="list_data_return"]/table/thead/tr/th[1]/text()').extract_first()
        #yield hdrinf

        #book information
        books = response.xpath ('//*[@id="list_data_return"]/table/tbody//tr')        
        publName = response.xpath('//select[@name="id_nxb"]/option[@selected]/text()').extract_first ()
        
			
        for book in books:
            bookinf = dict ()            
            if publName is not None:
                bookinf['PublisherName'] = publName.strip()
            bookinf['Seq'] = book.xpath ('td[1]/text()').extract_first()
            bookinf['ISBN'] = book.xpath ('td[2]/text()').extract_first()
            bookinf['Title'] = book.xpath ('td[3]/text()').extract_first()
            bookinf['Author'] = book.xpath ('td[4]/text()').extract_first()
            bookinf['Translator'] = book.xpath ('td[5]/text()').extract_first()
            bookinf['Nbr'] = book.xpath ('td[6]/text()').extract_first()
            bookinf['SelfPublished'] = book.xpath ('td[7]/text()').extract_first()
            bookinf['Partner'] = book.xpath ('td[8]/text()').extract_first()
            bookinf['PubIDNbr'] = book.xpath ('td[9]/text()').extract_first()            
            yield bookinf
        
        #goto the next page
        #for the next page url, we need to get the entire list then subtract by 1 
        l = len(response.xpath('//div[@class="pagination"]//ul/li/a/@href').extract ())
        if l>2: 
            next_page_url = response.xpath('//div[@class="pagination"]//ul/li/a/@href').extract ()[l-2] 
            if next_page_url is not None:
                 yield scrapy.Request(response.urljoin(next_page_url))

