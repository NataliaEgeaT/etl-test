import logging

def configure_logging():
    logging.basicConfig(
        level="INFO",
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
