from pydantic.v1 import BaseSettings, Field
import pymysql
from threading import Lock
from typing import ClassVar


class Settings(BaseSettings):
    TYPE_WORDS_STR: str = Field(default="玩具,手机", env="TYPE_WORDS_STR")
    MYSQL_HOST: str = Field(default="127.0.0.1", env="MYSQL_HOST")
    MYSQL_PORT: int = Field(default=3306, env="MYSQL_PORT")
    MYSQL_USER: str = Field(default="root", env="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(default="your password", env="MYSQL_PASSWORD")
    MYSQL_DATABASE: str = Field(default="e_commerce_spider", env="MYSQL_DATABASE")

    REDIS_HOST: str = Field(default="127.0.0.1", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    REDIS_PASSWORD: str = Field(default="your password", env="REDIS_PASSWORD")

    MAX_CONCURRENT_TYPE: int = Field(default=3, env="MAX_CONCURRENT_TYPE")
    MAX_CONCURRENT_SEARCH: int = Field(default=5, env="MAX_CONCURRENT_SEARCH")
    MAX_CONCURRENT_DETAIL: int = Field(default=2, env="MAX_CONCURRENT_DETAIL")

    NO_IMGS: bool = Field(default=False, env="NO_IMGS")
    NO_JS: bool = Field(default=False, env="NO_JS")
    HEADLESS: bool = Field(default=False, env="HEADLESS")
    PROXY: str = Field(default="", env="PROXY")

    ON_ECHO: bool = Field(default=False, env="ON_ECHO")  # 是否开启查询日志
    LOCK: ClassVar[Lock] = Lock()

    class Config:
        env_file = ".env"

    @property
    def MYSQL_PARAM(self) -> dict:
        return dict(
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            database=self.MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    @property
    def REDIS_PARAM(self) -> dict:
        return dict(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB,
            password=self.REDIS_PASSWORD,
        )


settings = Settings()
