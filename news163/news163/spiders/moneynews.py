# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

# lua_script = """
# function main(splash,args)
#     splash:go(args.url)
#     splash:wait(1)
#     splash:select("li.nav_item:nth-child(2)").mouse_hover({x=-2, y=-2})

#     splash:select(string.format("li.nav_item:nth-child(2)")).mouse_hover({x=-2, y=-2})

#     splash:wait(0.5)
#     splash:select("li.nav_item:nth-child(3)").mouse_hover({x=-2, y=-2})
#     splash:wait(0.5)
#     splash:select("li.nav_item:nth-child(4)").mouse_hover({x=-2, y=-2})
#     splash:wait(0.5)
#     splash:select("li.nav_item:nth-child(5)").mouse_hover({x=-2, y=-2})
#     splash:wait(0.5)
#     splash:select("li.nav_item:nth-child(6)").mouse_hover({x=-2, y=-2})
#     splash:wait(0.5)
#     splash:select("li.nav_item:nth-child(7)").mouse_hover({x=-2, y=-2})
#     splash:wait(0.5)
#     return splash:html()
# end
# """

lua_script = """
function main(splash,args)
    splash:go(args.url)
    splash:wait(1)
    ints = {2,3,4,5,6,7}
    for i,v in ipairs(ints) do
        splash:select(string.format("li.nav_item:nth-child(%d)",v)).mouse_hover({x=-2, y=-2})
        splash:wait(0.1)
    end
    return splash:html()
end
"""

class MoneynewsSpider(scrapy.Spider):
    name = 'moneynews'
    allowed_domains = ['money.163.com/']
    start_urls = ['http://money.163.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, endpoint='execute', args={'lua_source': lua_script})

    def parse(self, response):
        for sel in response.css('li.newsdata_item div.ndi_main')[:7]:
            title = sel.xpath('.//h3/a/text()').extract()[:5]
            #     # title=sel.xpath('string(.//h3/a)').extract_first()
            print(title)
