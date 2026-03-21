from utils.SqlacodegenUtil import gen_model
from settings import settings

if __name__ == "__main__":
    table_name = "goods3"
    model_file_name = f"{table_name[0].upper()}{table_name[1:]}Model"  # GoodsModel
    gen_model(
        database_name=settings.MYSQL_DATABASE,
        table_name=table_name,
        output_path=f"./models/{model_file_name}.py",
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD
    )
