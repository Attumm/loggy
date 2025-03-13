# Loggy Flask

Loggy Flask is a simple Flask application for logging and debugging. It provides HTTP endpoints to emit logs at various levels and includes a periodic logging mechanism for system status monitoring.

## Features

- Emit logs at different severity levels (debug, info, warning, error, critical)
- Control log frequency with the count parameter
- Trigger test crashes for monitoring and alerting verification
- Configurable periodic logging for system heartbeats
- Docker support for easy deployment

## Quick Start

### Using Docker

Build and run the application with Docker:

```bash
# Build the Docker image
docker build -t loggy_flask .

# Run the container
# Replace 'your_datadog_api_key' with your actual Datadog API key if using Datadog
docker run -d -p 8080:8000 -e DD_API_KEY=your_datadog_api_key -e DD_ENV=production loggy_flask

# Test that the application is running
curl 127.0.0.1:8080
```

### Running Locally

If you prefer to run the application locally without Docker:

```bash
# Install dependencies (requirements.txt should be in your project)
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage


### Using a Web Browser

Open your browser and navigate to:

- `http://127.0.0.1:8080/` - View application homepage 

### Using cURL

Emit logs at different levels:

```bash
# Log a message at INFO level
curl http://127.0.0.1:8080/info/system-startup/

# Log a warning message 3 times
curl http://127.0.0.1:8080/warning/disk-space-low/3

# Log a critical error
curl http://127.0.0.1:8080/critical/database-failure/
```


### Using Postman

1. Create a new GET request
2. Set the URL to one of the following formats:
   - `http://127.0.0.1:8080/{level}/{message}/` - To log a message once
   - `http://127.0.0.1:8080/{level}/{message}/{count}` - To log a message multiple times
3. Send the request

## Available Endpoints

- `/{level}/{message}/` - Log a message at the specified level
- `/{level}/{message}/{count}` - Log a message at the specified level multiple times
- `/crash/` - Trigger a controlled crash (caught exception)
- `/crash/fail` - Trigger an uncaught exception (for testing error handling)
- `/` - Application homepage with usage instructions

- `/health` - health check endpoint
- `ping` - returns pong, alternative healthcheck

### Log Levels

The following log levels are supported:

- `debug` - For detailed debugging information
- `info` - For general information
- `warning` - For warnings
- `error` - For error messages
- `critical` - For critical errors

## Configuration

The application uses the `settipy` library for configuration. You can configure:

- `PERIODIC_LOG_LEVEL` - Severity level for periodic logs (default: INFO)
- `PERIODIC_LOG_MESSAGE` - Message for periodic logs (default: "System heartbeat")
- `PERIODIC_LOG_INTERVAL` - Interval in seconds between periodic logs (default: 10)
- `HOST` - Host for the Flask webserver (default: 0.0.0.0)
- `PORT` - Port for the Flask webserver (default: 5000)
- `DEBUG` - Enable/Disable Flask debug mode (default: False)

You can set these via environment variables or command-line arguments.
