import inspect
import logging
import os

COLOR_GRAY = "\033[90m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_NORMAL = "\033[0m"
DEFAULT_COLOR_CODES = {
    logging.DEBUG: COLOR_GRAY,  # Grey
    logging.INFO: COLOR_GREEN,  # Green
    logging.WARNING: COLOR_YELLOW,  # Yellow
    logging.ERROR: COLOR_RED,  # Red
    logging.CRITICAL: COLOR_MAGENTA,  # Magenta
}


class CustomFormatter(logging.Formatter):
    color_codes = DEFAULT_COLOR_CODES
    RESET_COLOR_CODE = COLOR_GRAY

    def format(self, record):
        log_color = self.color_codes.get(record.levelno, self.RESET_COLOR_CODE)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET_COLOR_CODE}"

    def set_color_codes(self, color_codes):
        self.color_codes = color_codes


class ColoredLogger:
    __pattern: str
    __pattern_style: str
    __pattern_len: int
    __n_func_logs: int

    def __init__(
        self,
        name: str = None,
        level: int = 0,
        app_name: str = None,
        inspect_mode: bool = True,
        pattern_style: str = "-",
        pattern_len: int = 50,
        n_func_logs: int = 3,
    ) -> None:
        self.__inspect_mode = inspect_mode
        self.__n_func_logs = n_func_logs
        self.__set_patter(pattern_style, pattern_len)

        # Configure logging
        self.handler = logging.StreamHandler()
        self.formatter = CustomFormatter(self.__get_log_format(app_name))
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger(name)
        if level:
            self.logger.setLevel(level)
        self.logger.addHandler(self.handler)

    def __get_message_with_inspect(self, message: any, log_level: int = logging.INFO) -> str:
        inspected_logs: str = ""
        if self.__inspect_mode:
            inspected_logs = f"{COLOR_GRAY}"
            start_func = 2
            caller_frames = inspect.stack()
            down_way = self.__set_string_with_pattern("↓  ↓  ↓  ↓  ↓")
            funct_iter = list(range(start_func, self.__n_func_logs + start_func))
            funct_iter.reverse()
            for i in funct_iter:
                try:
                    caller_frame = caller_frames[i]
                    function_name = caller_frame.function
                    file_name = os.path.basename(caller_frame.filename)
                    line_number = caller_frames[i].lineno
                    inspected_logs += (
                        f"\nFile: {file_name} →  Function: {function_name} →  Line No: {line_number}\n{down_way}"
                    )
                except Exception:
                    continue
        inspected_logs += f"\n{[log_level]}{str(message)}\n"
        return inspected_logs

    def __get_log_format(self, app_name: str = None) -> str:
        heading = "%(asctime)s - %(levelname)s"
        if app_name:
            heading += f" {app_name} -"
        heading += " %(name)s -"
        heading = self.__set_string_with_pattern(heading)
        # Info: commented out because of the showing the message in normal format.
        # message = self.__set_string_with_pattern("- %(message)s -")
        message = "%(message)s"
        formated_string = (
            "\n"
            + COLOR_NORMAL
            + self.__pattern
            + COLOR_NORMAL
            + "\n"
            + COLOR_MAGENTA
            + heading
            + COLOR_NORMAL
            + "\n"
            + COLOR_GRAY
            + self.__pattern
            + COLOR_NORMAL
            + "\n"
            + message
            + COLOR_GRAY
            + "\n"
            + COLOR_GRAY
            + self.__pattern
            + COLOR_NORMAL
        )
        return formated_string

    def __set_patter(self, pattern_style: str, pattern_len: int) -> None:
        self.__pattern = pattern_style.join([pattern_style for _ in range(int(pattern_len / 2))])
        self.__pattern_len = len(self.__pattern)
        self.__pattern_style = pattern_style

    def __set_string_with_pattern(self, string: str):
        return f" {string} ".center(self.__pattern_len - 2, self.__pattern_style)

    def debug(self, message: any, **kwargs) -> None:
        self.logger.debug(self.__get_message_with_inspect(message, logging.DEBUG), **kwargs)

    def info(self, message: any, **kwargs) -> None:
        self.logger.info(self.__get_message_with_inspect(message, logging.INFO), **kwargs)

    def warning(self, message: any, **kwargs) -> None:
        self.logger.warning(self.__get_message_with_inspect(message, logging.WARNING), **kwargs)

    def error(self, message: any, **kwargs) -> None:
        self.logger.error(self.__get_message_with_inspect(message, logging.ERROR), **kwargs)

    def critical(self, message: any, **kwargs) -> None:
        self.logger.critical(
            self.__get_message_with_inspect(message, logging.CRITICAL),
            **kwargs,
        )

    def set_color_codes(
        self,
        debug: str = COLOR_GRAY,
        info: str = COLOR_GREEN,
        warning: str = COLOR_YELLOW,
        error: str = COLOR_RED,
        critical: str = COLOR_MAGENTA,
    ):
        self.formatter.set_color_codes(
            color_codes={
                logging.DEBUG: debug,
                logging.INFO: info,
                logging.WARNING: warning,
                logging.ERROR: error,
                logging.CRITICAL: critical,
            }
        )
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)


class SetColoredLogger:
    def __init__(
        self,
        log_level: int = 0,
        parent_name: str = None,
        inspect_mode: bool = True,
    ) -> None:
        self.level = log_level
        self.parent_name = parent_name
        self.inspect_mode = inspect_mode

    def get_logger(
        self,
        name: str = None,
        parent_name: str = None,
        inspect_mode: bool = None,
    ) -> ColoredLogger:
        parent_name = parent_name if parent_name else self.parent_name
        inspect_mode = inspect_mode if inspect_mode is not None else self.inspect_mode
        return ColoredLogger(name, self.level, parent_name, inspect_mode)
