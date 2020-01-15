# -*- coding: utf-8 -*-
import scrapy
import pandas

class RecopilacionDatosSymantec(scrapy.Spider):
    name = 'recopilacion-datos-symantec'    
    #https://cwe.mitre.org/top25/archive/2019/2019_cwe_top25.html
    start_urls = ['https://cwe.mitre.org/top25/archive/2019/2019_cwe_top25.html']    
    def parse(self, response):
        ataques = response.css('*[id=Detail] > tr')        
        for ataque in ataques:
            link = ataque.css('td > a::attr(href)').extract_first()             
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse_ataque)           
        
    def parse_ataque(self,response):
        nombreAtaque = response.css('div.noprint > h2::text').extract_first()
        descripcion = response.css('div[id=Description] > div.expandblock > div.detail > div.indent::text').extract_first()
        raintg = response.css('div[id=Likelihood_Of_Exploit] > div[id].expandblock > div.detail > div.indent::text').extract_first()
        f = open("datos_valores.data", "a")        
        f.write(str(nombreAtaque).strip()+"\t"+str(descripcion).strip()+"\t"+str(raintg).strip()+"\n")                
        f.close()

               	    
            	    
        

