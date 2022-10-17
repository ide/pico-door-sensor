import errno
import os

import storage
import supervisor

import adafruit_logging


_LOG_SIZE_THRESHOLD_BYTES = 100 * 1024**2


def create_logger() -> adafruit_logging.Logger:
    """Create the root logger and configure it to print all info messages and higher to stderr.
    Error messages and higher are written to a log file when the file system is writable.
    """
    logger = adafruit_logging.getLogger()
    logger.setLevel(adafruit_logging.INFO)

    if supervisor.runtime.usb_connected:
        logger.addHandler(adafruit_logging.StreamHandler())
    else:
        # The logging package prints messages with its default stream handler when the message is
        # too low in severity for any of the registered handlers. This null handler accepts messages
        # of all severity levels and suppresses the logger from writing high numbers of debug
        # messages through the default stream handler to stderr.
        logger.addHandler(adafruit_logging.NullHandler())

    log_filename = os.getenv("LOG_FILE")
    if log_filename and not storage.getmount("/").readonly:
        handler = _file_handler(logger, log_filename)
        handler.setLevel(adafruit_logging.ERROR)
        logger.addHandler(handler)

    return logger


def _file_handler(
    logger: adafruit_logging.Logger, log_filename: str
) -> adafruit_logging.FileHandler:
    # Prevent the log file from filling the flash memory
    log_file_mode = "a"
    try:
        size = os.stat(log_filename)[6]  # st_size is at index 6
        if size >= _LOG_SIZE_THRESHOLD_BYTES:
            log_file_mode = "w"
            logger.info("Log file is %d bytes, creating a new log file", size)
        else:
            logger.info("Log file is %d bytes, appending to existing log file", size)
    except OSError as error:
        if error.errno != errno.ENOENT:
            raise error
        log_file_mode = "w"
        logger.info("Log file does not exist, creating a new log file")

    return adafruit_logging.FileHandler(log_filename, mode=log_file_mode)
