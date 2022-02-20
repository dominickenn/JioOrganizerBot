from email import message
import logging
from operator import methodcaller

class Logger:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    @staticmethod
    def logMessageReceived(message: str, chat_id: str) -> None:
        logging.info(f"Received message: \'{message}\' from \'{chat_id}\'")

    @staticmethod
    def logMessageDispatch(message: str, chat_id: str) -> None:
        logging.info(f"Dispatching: \'{message}\' from \'{chat_id}\'")

    @staticmethod
    def buttonPressReceived(button_message: str, chat_id: str) -> None:
        logging.info(f"Button pressed: \'{button_message}\' from \'{chat_id}\'")

    @staticmethod
    def logSuccessfulOperation(message: str):
        logging.info(f"Successfully {message}")