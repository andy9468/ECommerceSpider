from typing import Union
from utils.MysqlUtil import MysqlUtil
session = MysqlUtil.get_session()
from models.GoodsModel import Goods
from utils.tools import create_uuid
from settings import settings

lock = settings.LOCK


def query_goods_by_name(title: str) -> Union[Goods, None]:
    """
    根据名称查询商品
    :param title: 名称
    :return: 商品或者None
    """
    result: Union[Goods, None] = session.query(Goods).filter_by(title=title).first()
    return result


def insert_goods(title: str, keyword: str, images: str, price: str, description: str, url: str) -> bool:
    """
    插入商品
    :param title: 名称
    :param keyword: 关键词
    :param images: 图片URL列表
    :param price: 价格
    :param description: 详情
    :param url: 商品详情连接
    :return: 是否成功插入
    """
    if query_goods_by_name(title=title):
        return True
    goods: Goods = Goods(
        title=title,
        keyword=keyword,
        images=images,
        price=price,
        url=url,
        description=description,
        uuid=create_uuid()
    )
    try:
        session.add(goods)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        return False
    return True
