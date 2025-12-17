# system_utils/logger.py

""" Import Library """
# Standard library imports
import atexit
import logging
import sys
import os
import warnings
from datetime import datetime


""" Custom Log Level """
# VERBOSE level: console output but not in info.log (for high-frequency iteration logs)
# Level hierarchy: DEBUG(10) < VERB(15) < FUTUREWARN(19) < INFO(20)
VERBOSE_LEVEL = 15
logging.addLevelName(VERBOSE_LEVEL, "VERB")

# Add custom log level for FutureWarning details
FUTURE_WARNING_LEVEL = 19
logging.addLevelName(FUTURE_WARNING_LEVEL, "FUTUREWARN")

# Shorten WARNING to WARN for compact display
logging.addLevelName(logging.WARNING, "WARN")

# Global flag to prevent duplicate log file location output
_log_files_printed = False


""" Log Filter """
class LevelFilter(logging.Filter):
    """Filter to log only specific level range.

    Used to separate debug logs from main logs.

    Args:
        min_level (int): Minimum log level (inclusive)
        max_level (int): Maximum log level (inclusive)
    """
    def __init__(self, min_level, max_level):
        super().__init__()
        self.min_level = min_level
        self.max_level = max_level

    def filter(self, record):
        """Only pass logs within the level range.

        Args:
            record (logging.LogRecord): Log record to filter

        Returns:
            passed (bool): True if record should be logged
        """
        return self.min_level <= record.levelno <= self.max_level


""" Logger Setup Function """
def setup_logger(name="GAIL", level=logging.INFO, log_dir="logs", console=True, file=True):
    """Setup logger with console and file outputs.

    Log Level Hierarchy:
        DEBUG(10) < VERBOSE(15) < FUTUREWARN(19) < INFO(20) < WARN(30) < ERROR(40)

    Log Level Routing:
        Level        | Console | info.log | verbose.log | debug.log
        -------------|---------|----------|-------------|----------
        DEBUG (10)   |    -    |    -     |      -      |    ✓
        VERBOSE (15) |    ✓    |    -     |      ✓      |    -
        INFO (20)+   |    ✓    |    ✓     |      -      |    -

    VERBOSE is ideal for high-frequency per-iteration logs that need
    real-time monitoring but would clutter info.log for post-analysis.

    Args:
        name (str): Logger name (default: "GAIL")
        level (int): Logging level for console (default: INFO)
        log_dir (str): Directory to save log files (default: "logs")
        console (bool): Enable console output (default: True)
        file (bool): Enable file output (default: True)

    Returns:
        logger (logging.Logger): Logger instance
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels

    # Avoid adding multiple handlers
    if logger.handlers:
        return logger


    """ Formatters """
    # Format: {time}; [{Log Level}]; [{python file name (fixed width)}]; {Message}
    # Using semicolon as delimiter for easier CSV parsing (comma is common in messages)
    # Filename is left-aligned with 24 char width for consistent alignment after semicolon
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s; [%(levelname)s]; [%(filename)-24s]; %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        fmt='%(asctime)s; [%(levelname)s]; [%(filename)-24s]; %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


    """ Console Handler """
    # Console handler - VERBOSE (15) and above (shows VERBOSE but not DEBUG)
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(VERBOSE_LEVEL)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)


    """ File Handlers """
    log_files = {}
    if file:
        # Create log directory if not exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Generate timestamp for file naming
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Main log file - INFO (20) and above
        main_log_file = os.path.join(log_dir, f'log_{timestamp}_info.log')
        main_handler = logging.FileHandler(main_log_file, mode='w', encoding='utf-8')
        main_handler.setLevel(logging.INFO)
        main_handler.setFormatter(detailed_formatter)
        logger.addHandler(main_handler)
        log_files['info'] = main_log_file

        # Verbose log file - VERBOSE level only (15)
        verbose_log_file = os.path.join(log_dir, f'log_{timestamp}_verbose.log')
        verbose_handler = logging.FileHandler(verbose_log_file, mode='w', encoding='utf-8')
        verbose_handler.setLevel(VERBOSE_LEVEL)
        verbose_handler.addFilter(LevelFilter(VERBOSE_LEVEL, VERBOSE_LEVEL))  # Only VERBOSE
        verbose_handler.setFormatter(detailed_formatter)
        logger.addHandler(verbose_handler)
        log_files['verbose'] = verbose_log_file

        # Debug log file - DEBUG level only (< VERBOSE)
        debug_log_file = os.path.join(log_dir, f'log_{timestamp}_debug.log')
        debug_handler = logging.FileHandler(debug_log_file, mode='w', encoding='utf-8')
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.addFilter(LevelFilter(0, VERBOSE_LEVEL - 1))  # Only logs < VERBOSE
        debug_handler.setFormatter(detailed_formatter)
        logger.addHandler(debug_handler)
        log_files['debug'] = debug_log_file

        # Log file location info will be logged after logger is created
        if console:
            # First log message indicating log file locations
            logger.info(f"Log files created:")
            logger.info(f"  - Main log: {main_log_file}")
            logger.info(f"  - Verbose log: {verbose_log_file}")
            logger.info(f"  - Debug log: {debug_log_file}")

    return logger, log_files



""" Warning Redirection """
def redirect_warnings_to_logger(logger_instance):
    """Redirect Python warnings to logger.

    Behavior:
    - FutureWarning: Summary at WARNING level, details at FUTUREWARN (19) level
    - Other warnings: Logged at WARNING level

    Args:
        logger_instance (logging.Logger): Logger instance to redirect warnings to
    """

    def warning_handler(message, category, filename, lineno, file=None, line=None):
        """Custom warning handler"""
        # Format the warning
        warning_msg = warnings.formatwarning(message, category, filename, lineno, line)

        if category == FutureWarning:
            # Summary for console/main log (WARNING level = 30)
            summary = f"FutureWarning in {filename}:{lineno}"
            logger_instance.warning(summary)

            # Detailed message for debug log (FUTUREWARN level = 19)
            logger_instance.log(FUTURE_WARNING_LEVEL, f"FutureWarning Details:\n{warning_msg.strip()}")
        else:
            # Other warnings go to WARNING level
            logger_instance.warning(warning_msg.strip())

    # Replace default warning handler
    warnings.showwarning = warning_handler


""" Custom Logger Wrapper """
class LoggerWrapper:
    """Wrapper class that adds to_cli option to logging methods.

    Provides same interface as logging.Logger but with optional to_cli parameter.
    When to_cli=False, logs only go to file handlers (skips console).

    Usage:
        logger = get_logger()
        logger.info("This goes to console and file")
        logger.info("This goes to file only", to_cli=False)

        # At script end
        logger.print_log_files()
    """

    # Log level name for file-only logging
    FILE_ONLY_LEVEL = 19  # Just below INFO (20), goes to debug.log

    def __init__(self, logger: logging.Logger, log_files: dict = None):
        self._logger = logger
        self._log_files = log_files or {}  # {"info": path, "verbose": path, "debug": path}

    def print_log_files(self):
        """Print log file locations (for use at script end)."""
        global _log_files_printed
        if self._log_files and not _log_files_printed:
            _log_files_printed = True
            self._logger.info("Log files:")
            for name, path in self._log_files.items():
                self._logger.info(f"  - {name}: {path}")

    def _log(self, level: int, msg: str, *args, to_cli: bool = True, stacklevel: int = 2, **kwargs):
        """Internal log method with to_cli support.

        Args:
            level: Log level (e.g., logging.INFO)
            msg: Log message
            to_cli: If False, log only to file (default: True)
            stacklevel: Stack level for caller info (default: 2 for wrapper methods)
            *args, **kwargs: Passed to logger
        """
        if to_cli:
            self._logger.log(level, msg, *args, stacklevel=stacklevel, **kwargs)
        else:
            # Log at FILE_ONLY_LEVEL to skip console (which filters >= INFO)
            # But preserve original level name in message for file
            level_name = logging.getLevelName(level)
            self._logger.log(self.FILE_ONLY_LEVEL, f"[{level_name}] {msg}", *args, stacklevel=stacklevel, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        """Log DEBUG message. Never goes to console (DEBUG < VERBOSE)."""
        self._logger.debug(msg, *args, stacklevel=2, **kwargs)

    def verbose(self, *args, to_cli: bool = True, **kwargs):
        """Log VERBOSE message. For high-frequency iteration logs.

        - Console: Yes (if to_cli=True)
        - info.log: No (VERBOSE < INFO)
        - debug.log: Yes

        Use for per-iteration status that needs real-time monitoring
        but would clutter info.log for post-analysis.

        Usage:
            logger.verbose("single message")
            logger.verbose("part1", "part2", "part3")  # joined with ", "
        """
        # Join multiple string arguments with ", "
        msg = ", ".join(str(arg) for arg in args)
        if to_cli:
            self._logger.log(VERBOSE_LEVEL, msg, stacklevel=2, **kwargs)
        else:
            self._logger.log(VERBOSE_LEVEL, msg, stacklevel=2, **kwargs)

    def info(self, msg: str, *args, to_cli: bool = True, **kwargs):
        """Log INFO message. Set to_cli=False to skip console output."""
        self._log(logging.INFO, msg, *args, to_cli=to_cli, stacklevel=3, **kwargs)

    def warning(self, msg: str, *args, to_cli: bool = True, **kwargs):
        """Log WARNING message. Set to_cli=False to skip console output."""
        self._log(logging.WARNING, msg, *args, to_cli=to_cli, stacklevel=3, **kwargs)

    def error(self, msg: str, *args, to_cli: bool = True, **kwargs):
        """Log ERROR message. Set to_cli=False to skip console output."""
        self._log(logging.ERROR, msg, *args, to_cli=to_cli, stacklevel=3, **kwargs)

    def critical(self, msg: str, *args, to_cli: bool = True, **kwargs):
        """Log CRITICAL message. Set to_cli=False to skip console output."""
        self._log(logging.CRITICAL, msg, *args, to_cli=to_cli, stacklevel=3, **kwargs)

    def log(self, level: int, msg: str, *args, to_cli: bool = True, **kwargs):
        """Log at specified level. Set to_cli=False to skip console output."""
        self._log(level, msg, *args, to_cli=to_cli, stacklevel=3, **kwargs)

    def exception(self, msg: str, *args, to_cli: bool = True, **kwargs):
        """Log ERROR with exception info. Set to_cli=False to skip console output."""
        kwargs['exc_info'] = kwargs.get('exc_info', True)
        self._log(logging.ERROR, msg, *args, to_cli=to_cli, stacklevel=3, **kwargs)

    # Delegate other attributes to underlying logger
    def __getattr__(self, name):
        return getattr(self._logger, name)


""" Global Logger Instance """
# Create global logger
_raw_logger, _log_files = setup_logger()
logger = LoggerWrapper(_raw_logger, _log_files)

# Redirect warnings to logger
redirect_warnings_to_logger(_raw_logger)

# Register atexit handler only in main process (not in child processes)
# Child processes from multiprocessing have different parent process
import multiprocessing
if multiprocessing.current_process().name == 'MainProcess':
    atexit.register(logger.print_log_files)


""" Logger Access Function """
def get_logger(name=None, **kwargs) -> LoggerWrapper:
    """Get logger instance with to_cli support.

    Args:
        name (Optional[str]): Logger name (if None, returns global logger)
        **kwargs: Additional arguments for setup_logger

    Returns:
        LoggerWrapper: Logger instance with to_cli option

    Usage:
        logger = get_logger()
        logger.info("Normal log")              # Console + file
        logger.info("File only", to_cli=False) # File only

        # At script end
        logger.print_log_files()
    """
    if name:
        raw_logger, log_files = setup_logger(name, **kwargs)
        return LoggerWrapper(raw_logger, log_files)
    return logger

# EOS - End of Script
