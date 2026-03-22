import time
import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from DrissionPage import ChromiumPage, ChromiumOptions
from settings import settings

HEADLESS = settings.HEADLESS
NO_IMGS = settings.NO_IMGS
NO_JS = settings.NO_JS
PROXY = settings.PROXY


class BaseMultiTabSpider(ABC):
    """
    多标签页爬虫基类

    功能：
    1. 创建单个浏览器实例
    2. 管理多个标签页
    3. 控制并发数量
    4. 提供异步执行框架
    """

    def __init__(self,
                 max_concurrent: int = 3,
                 browser_options: Optional[ChromiumOptions] = None,
                 proxy: Optional[str] = None,
                 ):
        """
        初始化基类

        Args:
            max_concurrent: 最大并发标签页数量
            browser_options: 浏览器配置选项，为 None 时使用默认配置
        """
        self.proxy = proxy
        self.browser_options = browser_options

        self.semaphore = asyncio.Semaphore(max_concurrent)

    def do_init(self):
        if self.browser_options is None:
            self.browser_options = self._default_browser_options()

        self.browser = self.create_browser()

    def _default_browser_options(self) -> ChromiumOptions:
        """默认的浏览器配置"""
        co = ChromiumOptions()
        co.headless(HEADLESS)
        co.no_imgs(NO_IMGS)
        co.no_js(NO_JS)
        co.set_argument('--disable-gpu')
        co.set_argument('--no-sandbox')
        co.set_argument('--disable-dev-shm-usage')
        if PROXY:
            self.proxy = PROXY
        if self.proxy:
            co.set_argument(f'--proxy-server={self.proxy}')

        return co

    def create_browser(self) -> ChromiumPage:
        """创建浏览器实例"""
        browser = ChromiumPage(self.browser_options)

        return browser

    def find_flag_element(self, tab, timeout: int = 10) -> Optional[Any]:
        """查找标记元素"""
        ...

    @abstractmethod
    def do_something_in_tab(self, tab, *args, **kwargs) -> Optional[Any]:
        """在标签页中执行具体任务"""
        ...
        return tab

    @abstractmethod
    def do_something_out_of_tab(self, html, *args, **kwargs) -> Optional[Any]:
        """在标签页外执行具体任务"""
        print("在标签页外执行具体任务...")
        ...
        return html

    def open_tab(self,
                 url: str,
                 timeout: int = 10,
                 *args,
                 **kwargs
                 ) -> Optional[Any]:
        """打开一个新的标签页"""

        html = ''
        try:
            tab = self.browser.new_tab()

            flag = tab.get(url, timeout=timeout)

            self.find_flag_element(tab)

            tab = self.do_something_in_tab(tab, *args, **kwargs)

            if flag:
                html = tab.html

                self.close_tab_safe(tab)

                r = self.do_something_out_of_tab(html, *args, **kwargs)
            else:
                print(f"任务执行失败：{url}")

        except Exception as e:
            print(f"任务执行失败：{e}")
            raise

        finally:
            self.close_tab_safe(tab)

            return html

    def close_tab_safe(self, tab):
        try:
            tab.close()
            print("关闭标签页 ok")
        except Exception as e:
            pass

    def close_browser(self):
        """关闭浏览器"""
        if hasattr(self, 'browser'):
            try:
                self.browser.quit()
                print("浏览器已关闭")
            except Exception as e:
                print(f"关闭浏览器失败：{e}")

    async def async_open_tab(self, *args, **kwargs):
        async with self.semaphore:
            loop = asyncio.get_event_loop()

            result = await loop.run_in_executor(
                None,
                lambda: self.open_tab(*args, **kwargs)
            )
            html = result

        return html


class BaiduMultiTabSpider(BaseMultiTabSpider):
    """百度搜索爬虫实现类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.do_init()

    def find_flag_element(self, tab, timeout: int = 10) -> Optional[Any]:
        flag_element = tab.wait.ele_displayed('#kw', timeout=timeout)
        return flag_element

    def do_something_in_tab(self, tab, *args, **kwargs) -> Optional[Any]:
        word = kwargs.get('word', 'python')

        keyword_input = tab.wait.ele_displayed('#kw', timeout=10)
        if keyword_input:
            keyword_input.input(word)
            tab.ele('#chat-submit-button').click()
            time.sleep(3)

        return tab

    def do_something_out_of_tab(self, html, *args, **kwargs) -> Optional[Any]:
        len_html = len(html)
        print(" 在标签页外执行具体任务 >>> 耗时操作")
        time.sleep(3)

        return len_html


async def main():
    sp = BaiduMultiTabSpider(3)

    url = 'https://www.baidu.com'
    words = ['python', 'java', 'c++', 'go', 'rust']

    tasks = [sp.async_open_tab(url, word=word) for word in words]


    results = []
    for task in asyncio.as_completed(tasks):
        result = await task
        results.append(result)
        print(f"获取到结果，长度：{len(result)}")

    for result in results:
        print(len(result))
    sp.close_browser()


if __name__ == '__main__':
    print(f"开始执行任务，请稍候...")
    pass
    asyncio.run(main())
    pass
