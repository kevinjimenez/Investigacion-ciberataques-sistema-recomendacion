# -*- coding: utf-8 -*-
import scrapy
import pandas

class RecopilacionDatosSymantec(scrapy.Spider):
    name = 'recopilacion-datos-symantec'    
    start_urls = ['https://www.symantec.com/security_response/attacksignatures/']    
    def parse(self, response):
        ataques = response.css('div > .size1of2')                	    
        for ataque in ataques:                        
            attack = ataque.css('a')            
            for item in attack:                
                link_ataque = item.css('a::attr(href)').extract_first()       
                next_page = response.urljoin(link_ataque)
                yield scrapy.Request(next_page, callback=self.parse_ataque)

    def parse_ataque(self,response):
        valor = []        
        tipoAtaque = response.css('.contentPane > h1::text').extract_first()        
        raiting = response.css('div > .bckPadLG > h3::text').extract_first()
        descripcionRaiting = response.xpath('//div[@class="bckPadLG bckSolidWht unit"]/text()').getall()                        
        f = open("ataques_raiting.data", "a")        
        f.write(str(tipoAtaque).strip()+"\t"+str(raiting).strip()+"\t"+str(descripcionRaiting[1]).strip()+"\n")                
        f.close()
        a = response.css('div > .bckPadLG > .cbMrgnTopLG::text').getall()

        """for aa in a:  
            t = aa.css('*::text').getall()            
            valor.append(t);                         
            #print(t, len(t), type(t))        """
        print(a)
            
        #f = open("data_sets.data", "a")        
        #f.write(str(tipoAtaque).strip()+"\t"+str(descripcionAtaque[1]).strip()+"\t"+str(raiting).strip()+"\t"+str(descripcionRaiting[1]).strip()+"\n")                
        #f.close()

