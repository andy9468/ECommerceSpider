from models import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from settings import settings


class MysqlUtil(object):
    connect_uri: str = f"mysql+pymysql://" \
                       f"{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@" \
                       f"{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/" \
                       f"{settings.MYSQL_DATABASE}"
    engine: Engine = create_engine(url=connect_uri, echo=settings.ON_ECHO)

    SessionLocal: sessionmaker = sessionmaker(bind=engine)

    @staticmethod
    def create_tables() -> None:
        """
        创建数据表（如果不存在）
        :return:
        """
        BaseModel.metadata.create_all(MysqlUtil.engine, checkfirst=True)

    @staticmethod
    def get_session() -> Session:
        """
        获取新的 sqlalchemy session，用于操作数据库
        每次调用都会创建新的 session 实例，避免并发冲突
        :return: Session 对象
        """
        return MysqlUtil.SessionLocal()



