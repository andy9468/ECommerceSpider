from uuid import uuid4


def create_uuid() -> str:
    """
    创建UUID
    :return: UUID字符串
    """
    return str(uuid4()).replace("-", "")
