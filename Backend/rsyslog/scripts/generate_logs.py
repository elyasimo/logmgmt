import logging
import random

def generate_log(logger, level, message):
    if level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.critical(message)

if __name__ == "__main__":
    logging.basicConfig(filename='generated_logs.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    messages = [
        "User login successful",
        "Failed login attempt",
        "Database connection error",
        "API request received",
        "File not found"
    ]

    for _ in range(100):
        level = random.choice(levels)
        message = random.choice(messages)
        generate_log(logger, level, message)

