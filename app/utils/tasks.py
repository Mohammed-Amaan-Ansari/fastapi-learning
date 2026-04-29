from app.utils.logger import logger
import time


def log_todo_creation(user_id: int, title: str):
    # Simulate delay
    time.sleep(2)

    logger.info(f"[BACKGROUND] User {user_id} created todo: {title}")