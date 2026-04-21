import pandas as pd
from sqlalchemy import create_engine
import logging
import time
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SOURCE_CONN = (
    f"postgresql://{os.getenv('DB_SOURCE_USERNAME')}:{os.getenv('DB_SOURCE_PASSWORD')}"
    f"@{os.getenv('HOST_SOURCE')}:{os.getenv('PORT_SOURCE')}/{os.getenv('DB_SOURCE')}"
)

TARGET_CONN = (
    f"postgresql://{os.getenv('DB_TARGET_USERNAME')}:{os.getenv('DB_TARGET_PASSWORD')}"
    f"@{os.getenv('HOST_TARGET')}:{os.getenv('PORT_TARGET')}/{os.getenv('DB_TARGET')}"
)

def main():
    try:
        start_time = time.time()
        logger.info("Начало загрузки данных")

        source_engine = create_engine(SOURCE_CONN)
        logger.info("Подключение к источнику успешно")

        df = pd.read_sql("SELECT * FROM bookings.mart_route_sales", source_engine)
        logger.info(f"Прочитано строк из источника: {len(df)}")

        target_engine = create_engine(TARGET_CONN)
        logger.info("Подключение к приёмнику успешно")

        df.to_sql(
            name="mart_route_sales",
            con=target_engine,
            if_exists="replace",
            index=False
        )

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"Загружено строк: {len(df)}")
        logger.info(f"Время выполнения: {elapsed} сек")

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
