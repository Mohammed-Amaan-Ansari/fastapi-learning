import logging

# Create logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.propagate = False

# Format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

# Add handlers (avoid duplicate adding)
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)