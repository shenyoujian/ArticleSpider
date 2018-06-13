# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    # start_urls是一个待爬取的列表.
    # spider会为我们请求下载网页，直接到parse阶段
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1、获取文章列表页中的文章url并交给scrapy下载后进行解析
        2、获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        '''
        # 解析所有列表页的所有文章url并交给scrapy下载后并解析
        # 注意不止获取我们的目标url，还会获取多余的url，我们需要过滤
        # 我们可以往上在找一个独一的属性,注意id属性使用#
        # post_urls = response.css(".floated-thumb .post-thumb a::attr(href)").extract_first()
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            # 注意有些url是没有域名的，只有简单1，2，这是我们得加上域名
            # 然后回调函数只需要给个函数它自己就会去调用
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.detail_parse)
        # 获取下一页链接并交给scrapy下载
        # .next.page-number是两个class一起的
        # 回调函数不在是detail而是parse
        next_url = response.css(".next.page-numbers::attr(href)")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
        pass


    def detail_parse(self, response):
        # 使用xpath提取文章的具体字段
        # 注意不要使用/html/....有时候会取不到，因为会有ajax或者js动态生成的元素
        # 然后要用extract_first(""),因为如果用extract()[0]数组下标取不到会报错
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first().strip().replace("·","").strip()
        # praise_nums = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract_first(""))
        # if not praise_nums:
        #     praise_nums = 0
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first()
        # match_re = re.match(".*?(\d+).*", fav_nums)             # 注意加个？，没加会贪婪匹配
        # if match_re:                                            # 假如是11个收藏，它从有匹配到个1就结束了而不是11
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # content = response.xpath("//div[@class='entry']").extract_first()
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)



        # 使用css选择器提取文章具体字段
        # .entry-header 选择class属性为entry-header的所有元素
        title = response.css(".entry-header h1::text").extract_first()
        create_date = response.css(".entry-meta-hide-on-mobile::text").extract_first().strip().replace("·", "").strip()
        praise_nums = int(response.css(".vote-post-up h10::text").extract_first())
        if not praise_nums:
            praise_nums = 0
        fav_nums = response.css(".bookmark-btn::text").extract_first()
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        # 选择所有href='#article-comment'的所有a属性
        comment_nums = response.css("a[href='#article-comment'] span::text").extract_first()
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        # 选择所有class=entry的div元素
        content = response.css("div.entry").extract_first()
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        pass



















