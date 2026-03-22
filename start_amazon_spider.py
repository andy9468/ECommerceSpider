import asyncio

from spiders.AmazonSpider import main_amazon_spider


async def main():
    await main_amazon_spider()


if __name__ == '__main__':
    asyncio.run(main())
