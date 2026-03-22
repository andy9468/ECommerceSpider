import urllib
import asyncio
from typing import List, Dict, Any, Optional

from dbcontrol.GoodsCtr import insert_goods

from utils.TabSpider import BaseMultiTabSpider
from lxml.html import Element
from lxml import etree
from settings import settings


class AmazonTypeSpider(BaseMultiTabSpider):
    """亚马逊类别爬虫实现类
    输入商品类别，获取某个类别下的所有搜索页面url
    例如：玩具
    获取：玩具搜索页 1
         玩具搜索页 2
         玩具搜索页 n
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.do_init()
        self.total_search_pages = []
        pass

    def find_flag_element(self, tab, timeout: int = 10) -> Optional[Any]:
        flag_element = tab.wait.ele_displayed('.s-list-item-margin-right-adjustment', timeout=timeout)
        ...
        return flag_element

    def do_something_in_tab(self, tab, *args, **kwargs) -> Optional[Any]:
        kw = kwargs.get('kw', 'python')
        print(f"开始执行任务：{kw}")

        element: Element = etree.HTML(text=tab.html)

        total_pages_list = element.xpath(
            "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator']/../../preceding-sibling::li[1]/span/a | //a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator']/../../preceding-sibling::span[1]"
        )
        if len(total_pages_list) > 1:
            total_pages = int(total_pages_list[-1].text)
        else:
            total_pages = int(total_pages_list[0].text)

        all_page_url: list[str] = []

        next_page_url: str = element.xpath(
            '//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator"]/@href')[
            0]
        for page_size in range(1, total_pages + 1):
            before_url: str = next_page_url.split("page=")[0]  # 前部分URL
            back_url: str = next_page_url.split("page=")[-1][1:]  # 去掉页码后的URL
            result_url: str = "https://www.amazon.com" + before_url + "page=" + str(page_size) + back_url  # 拼接后的URL
            result_url = result_url.replace("/-/zh", "").split("&qid")[0] + "&s=relevanceblender"
            all_page_url.append(result_url)

        self.total_search_pages.extend(all_page_url)

        return tab

    def do_something_out_of_tab(self, html, *args, **kwargs) -> Optional[Any]:
        len_html = len(html)

        return len_html

    async def get_total_search_urls(self, base_url, keywords):
        search_urls = [base_url + kw for kw in keywords]
        tasks = [self.async_open_tab(url, kw=kw) for url, kw in zip(search_urls, keywords)]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)

        return self.total_search_pages


class AmazonSearchSpider(BaseMultiTabSpider):
    """亚马逊搜索爬虫实现类
    访问一个搜索页面，获取其中的全部详情页面cards
    例如：玩具搜索页 2

    访问：玩具搜索页 2
    获取：所有商品的cards
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.do_init()
        self.cur_search_url = ""
        self.cur_goods_cards = []
        self.cur_all_goods_urls = []
        pass

    def find_flag_element(self, tab, timeout: int = 10) -> Optional[Any]:
        ...

    def do_something_in_tab(self, tab, *args, **kwargs) -> Optional[Any]:
        cur_all_goods_urls: list[str] = self.get_cur_all_goods_urls(tab.html)
        self.cur_all_goods_urls = cur_all_goods_urls

        return tab

    def do_something_out_of_tab(self, html, *args, **kwargs) -> Optional[Any]:
        len_html = len(html)

        return len_html

    def get_goods_cards(self, html: str) -> Optional[list[Element]]:
        """
        获取所有商品板块元素
        :param html: HTML源码
        :return: 商品板块元素列表
        """
        element: Element = etree.HTML(text=html)
        goods_cards: list[Element] = element.xpath(
            '//div[@class="sg-col-inner"]//div[@class="a-section a-spacing-base desktop-grid-content-view"]')

        return goods_cards

    def get_cur_all_goods_urls(self, html: str) -> Optional[Any]:
        """
        获取所有商品板块元素
        :param html: HTML源码
        :return: 商品板块元素列表
        """
        cur_all_goods_urls = []
        element: Element = etree.HTML(text=html)
        d_urls: list[Element] = element.xpath(
            "//div[@cel_widget_id]//div[contains(@class,'a-section')]//h2/span/../../@href")

        for d_url in d_urls:
            if d_url.startswith("/"):
                detail_url = "https://www.amazon.com" + d_url
            else:
                detail_url = d_url
            cur_all_goods_urls.append(detail_url)


        return cur_all_goods_urls


class AmazonDetailSpider(BaseMultiTabSpider):
    """亚马逊搜索爬虫实现类
    访问一个搜索页面，获取其中的全部详情页面cards
    例如：玩具搜索页 2

    访问：玩具搜索页 2
    获取：所有商品的cards
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.do_init()
        self.detail_dict = {}
        self.cur_total_detail_data = []
        pass

    def find_flag_element(self, tab, timeout: int = 10) -> Optional[Any]:
        ...

    def do_something_in_tab(self, tab, *args, **kwargs) -> Optional[Any]:
        detail_dict: list[str] = self.parse_detail(tab.html, *args, **kwargs)
        self.detail_dict = detail_dict
        if detail_dict:
            try:
                if insert_goods(**detail_dict):
                    print(f"存储成功：{detail_dict}")
            except TimeoutError as e:
                print(e)

        return tab

    def do_something_out_of_tab(self, html, *args, **kwargs) -> Optional[Any]:
        len_html = len(html)

        return len_html

    def get_goods_cards(self, html: str) -> Optional[list[Element]]:
        """
        获取所有商品板块元素
        :param html: HTML源码
        :return: 商品板块元素列表
        """
        element: Element = etree.HTML(text=html)
        goods_cards: list[Element] = element.xpath(
            '//div[@class="sg-col-inner"]//div[@class="a-section a-spacing-base desktop-grid-content-view"]')

        return goods_cards

    def parse_detail(self, html: str, *args, **kwargs) -> Optional[Any]:
        """
        获取所有商品板块元素
        :param html: HTML源码
        :return: 商品板块元素列表
        """
        detail_dict = {
            "keyword": "",
            "title": "",
            "images": "",
            "price": "",
            "url": "",
            "description": "",
        }

        detail_url = kwargs.get('detail_url', '')

        if detail_url:
            detail_url_zh = urllib.parse.unquote(urllib.parse.unquote(detail_url))
            detail_dict["keyword"] = detail_url_zh.partition("&keywords=")[-1].partition("&")[0]
            detail_dict["url"] = detail_url

        element: Element = etree.HTML(text=html)
        title: str = element.xpath("//span[@id='productTitle']/text()")[0].strip(" ")
        images_div = element.xpath('//div[@id="imageBlock"]//div[@id="altImages"]/following-sibling::div[1]')[0]
        images_list = images_div.xpath('//span[@data-action="main-image-click"]//img[@alt]/@src')
        images = ",".join(images_list)
        price: str = element.xpath('//span[@id="apex-pricetopay-accessibility-label"]/text()')[0].strip(" ").strip("$")
        if " " in price:
            price = price.split(" ")[0]
        description_list = element.xpath("//div[@id='feature-bullets']/ul/li/span/text()")
        description: str = "\n".join([i.strip(" ") for i in description_list])

        detail_dict["title"] = title
        detail_dict["images"] = images
        detail_dict["price"] = price
        detail_dict["description"] = description

        self.detail_dict = detail_dict
        self.cur_total_detail_data.append(detail_dict)

        return detail_dict

    async def get_cur_total_detail_data(self, cur_all_goods_urls):
        tasks = [self.async_open_tab(url, detail_url=url) for url in cur_all_goods_urls]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)

        return self.detail_dict


async def main_amazon_spider():
    sp_type = AmazonTypeSpider(settings.MAX_CONCURRENT_TYPE)

    base_url = 'https://www.amazon.com/s?k='
    keywords = settings.TYPE_WORDS_STR.split(",")
    total_search_urls = await sp_type.get_total_search_urls(base_url, keywords)
    print(total_search_urls)
    print(f"所有搜索页面urls总数：{len(total_search_urls)}")

    sp_type.close_browser()

    for i, search_url in enumerate(total_search_urls):
        sp_search = AmazonSearchSpider(settings.MAX_CONCURRENT_SEARCH)

        detail_html = await sp_search.async_open_tab(search_url)
        cur_all_goods_urls = sp_search.cur_all_goods_urls
        print(f"【{i + 1}/{len(total_search_urls)}】 开始采集当前页面的 {len(cur_all_goods_urls)} 个商品 的 详情页面数据")
        print(search_url)

        sp_search.close_browser()

        sp_detail = AmazonDetailSpider(settings.MAX_CONCURRENT_DETAIL)

        detail_html = await sp_detail.get_cur_total_detail_data(cur_all_goods_urls)
        cur_total_detail_data = sp_detail.cur_total_detail_data
        print(cur_total_detail_data)
        print(len(cur_total_detail_data))

        sp_detail.close_browser()
        pass


if __name__ == '__main__':
    asyncio.run(main_amazon_spider())
