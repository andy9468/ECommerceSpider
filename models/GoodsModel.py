from typing import Optional
import datetime
import decimal

from sqlalchemy import DECIMAL, DateTime, text
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseModel


class Goods(BaseModel):
    __tablename__ = 'goods'

    uuid: Mapped[str] = mapped_column(VARCHAR(32), primary_key=True, comment='主键')
    keyword: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='商品关键词')
    title: Mapped[Optional[str]] = mapped_column(VARCHAR(200), comment='商品标题')
    images: Mapped[Optional[str]] = mapped_column(TEXT, comment="商品图片列表，用英文','分割")
    price: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='商品单价')
    url: Mapped[Optional[str]] = mapped_column(TEXT, comment='商品详情页地址')
    description: Mapped[Optional[str]] = mapped_column(LONGTEXT, comment='商品详情')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False,
                                                          server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')
