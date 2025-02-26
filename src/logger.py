import logging

class Logger:
    _logger = None  # Class-level logger instance

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._initialize_logger()
        return cls._logger
    
    @classmethod
    def _initialize_logger(cls):
        """Initialize the logger with a standard configuration."""
        cls._logger = logging.getLogger(__name__)
        cls._logger.setLevel(logging.DEBUG) 

        file_handler = logging.FileHandler('app.log',)
        file_handler.setLevel(logging.DEBUG)

        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        # console_handler.setFormatter(formatter)

        cls._logger.addHandler(file_handler)
        # cls._logger.addHandler(console_handler)
