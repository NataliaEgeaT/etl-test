import json
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class APIClient:
    """Reads API mock JSON file but simulates API errors with retry logic."""

    def __init__(self, file_path, retries=3, retry_delay=1):
        self.file_path = Path(file_path)
        self.retries = retries
        self.retry_delay = retry_delay

    def get_orders(self):
        attempts = 0

        while attempts < self.retries:
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)

                logger.info(f"Loaded {len(data)} raw orders from API mock")
                return data

            except Exception as exc:
                attempts += 1
                logger.warning(
                    f"API Mock read failed (Attempt {attempts}/{self.retries}): {exc}"
                )
                time.sleep(self.retry_delay)

        raise RuntimeError("API Mock could not be read after maximum retries")
