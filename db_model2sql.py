"""
对象转数据表
"""
from utils.MysqlUtil import MysqlUtil

if __name__ == "__main__":
    from models.GoodsModel import Goods

    MysqlUtil.create_tables()
