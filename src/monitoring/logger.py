import logging
import os


os.makedirs(
    "logs",
    exist_ok=True
)

logging.basicConfig(

    filename="logs/predictions.log",

    level=logging.INFO,

    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(message)s"
    )
)

prediction_logger = logging.getLogger(
    "prediction_logger"
)