import logging
class APILog:
    def __init__(self, log_file="app.log"):
        self.logger = logging.getLogger("AppLogger")

        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)

            # File Handler (without colors)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(file_handler)

            # Stream Handler (with full-line colors)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(self._get_colored_formatter())
            self.logger.addHandler(stream_handler)

    def _get_colored_formatter(self):
        """Returns a formatter that applies color to the entire log line."""
        class FullLineColoredFormatter(logging.Formatter):
            COLORS = {
                logging.DEBUG: "\033[94m",    # Blue
                logging.INFO: "\033[92m",     # Green
                logging.WARNING: "\033[93m",  # Yellow
                logging.ERROR: "\033[91m",    # Red
                logging.CRITICAL: "\033[95m", # Magenta
            }
            RESET = "\033[0m"  # Reset color

            def format(self, record):
                color = self.COLORS.get(record.levelno, self.RESET)
                formatted = super().format(record)
                return f"{color}{formatted}{self.RESET}"

        return FullLineColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_exception(self, exception):
        self.logger.exception(exception)
