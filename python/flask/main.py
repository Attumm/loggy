"""
Logger Service - A simple Flask application for logging and debugging.

This service provides HTTP endpoints to emit logs at various levels and
a periodic logging mechanism for system status monitoring.
"""


from flask import Flask
import logging
import sys
import os
import time
import threading

from settipy import settipy

app = Flask(__name__)

# Configure logging (keep this outside as it's general logging setup)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

log_levels = {
    "debug": logger.debug,
    "info": logger.info,
    "warning": logger.warning,
    "error": logger.error,
    "critical": logger.critical
}


# Define periodic_logger and routes outside, as they are part of the app's structure
def periodic_logger():
    while True:
        time.sleep(settipy["PERIODIC_LOG_INTERVAL"]) # Access directly using settipy["VAR_NAME"]
        log_function = log_levels.get(settipy["PERIODIC_LOG_LEVEL"].lower(), logger.info) # Access directly
        log_function(settipy["PERIODIC_LOG_MESSAGE"]) # Access directly


@app.route('/health')
def health():
    return "", 204


@app.route('/ping')
def ping():
    return "pong", 200


@app.route('/<level>/<message>/')
@app.route('/<level>/<message>/<int:count>')
def log_message_route(level, message, count=1):
    """
    Endpoint to emit logs via HTTP requests.

    Parameters:
        level (str): The log level to use (debug, info, warning, error, critical)
        message (str): The message to log
        count (int, optional): Number of times to emit the log. Defaults to 1.

    Returns:
        tuple: A response message and HTTP status code

    Example:
        GET /info/system-startup/ - Logs "system-startup" at INFO level once
        GET /error/database-connection-failed/5 - Logs error message 5 times
    """
    if level.lower() not in log_levels:
        return f"Invalid log level: {level}. Must be one of: {', '.join(log_levels.keys())}", 400
    log_function = log_levels[level.lower()]
    for _ in range(count):
        log_function(message)
    return f"Emitted {count} logs at level {level.upper()} with message: {message}"


@app.route('/crash/')
@app.route('/crash/<handle>')
def crash_route(handle=""):
    """
    Debug endpoint that triggers a division by zero error.

    Used for testing error handling and logging in production/staging environments.

    Parameters:
        handle (str, optional): If set to 'false', 'f', 'no', 'n', or 'fail', 
                               the exception will be propagated instead of caught.
                               Default is to catch the exception.

    Returns:
        tuple: A response message and HTTP status code

    Raises:
        ZeroDivisionError: When handle parameter indicates the error should not be caught
    """
    try:
        _ = 1 / 0
    except ZeroDivisionError:
        logger.critical("Application crash initiated due to division by zero!")
        if handle.lower() in {"false", "f", "no", "n", "fail"}:
            raise
        return "Crash endpoint triggered! Check server logs for division by zero error.", 500
    return "This should not be returned as crash is intended", 200


@app.route('/')
def default_route():
    """
    Default route that serves as the application's homepage.

    Returns information about the available endpoints and their usage.

    Returns:
        str: HTML content describing the API endpoints
    """
    return open("index.html").read()


if __name__ == '__main__':
    settipy.set("PERIODIC_LOG_LEVEL", "INFO", "Severity level for periodic logs (INFO, WARNING, ERROR, etc.)")
    settipy.set("PERIODIC_LOG_MESSAGE", "System heartbeat", "Message for periodic logs")
    settipy.set_int("PERIODIC_LOG_INTERVAL", 10, "Interval in seconds between periodic logs")
    settipy.set("HOST", "0.0.0.0", "Host for the Flask webserver")
    settipy.set_int("PORT", 8000, "Port for the Flask webserver")
    settipy.set_bool("DEBUG", False, "Enable/Disable Flask debug mode")

    settipy.parse(verbose=True)

    startup_vars = {
        "script_name": os.path.basename(__file__),
        "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "periodic_log_level": settipy["PERIODIC_LOG_LEVEL"],
        "periodic_log_message": settipy["PERIODIC_LOG_MESSAGE"],
        "periodic_log_interval": settipy["PERIODIC_LOG_INTERVAL"],
        "flask_host": settipy["HOST"],
        "flask_port": settipy["PORT"],
        "flask_debug": settipy["DEBUG"]
    }
    logger.info(f"Project started with these vars: {startup_vars}")

    # Start the periodic logger in a background thread
    periodic_log_thread = threading.Thread(target=periodic_logger, daemon=True)
    periodic_log_thread.start()

    app.run(debug=settipy["DEBUG"], host=settipy["HOST"], port=settipy["PORT"])
