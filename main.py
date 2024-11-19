from aiohttp import web
import datetime

# Global log data
logs = []

# Handler for logging humidity data
async def log_data(request):
    try:
        # Get JSON data from request
        data = await request.json()
        
        # Check if temperature data is provided
        if 'temperature' in data:
            temperature = data['temperature']
            timestamp = datetime.datetime.now()
            log_entry = f"Temperature: {temperature}% - Time: {timestamp}"
            logs.append(log_entry)
            return web.json_response({"status": "success", "message": "Temperature data received."})
        else:
            # Log error if data is not in the expected format
            logs.append("Error: Received invalid data.")
            return web.json_response({"status": "error", "message": "Invalid data format."}, status=400)
    except Exception as e:
        # Log exception if JSON parsing fails
        logs.append(f"Error: {str(e)}")
        return web.json_response({"status": "error", "message": "Invalid request."}, status=400)

# Handler for resetting logs
async def reset_logs(request):
    global logs
    logs = []
    return web.json_response({"status": "success", "message": "Logs have been reset."})

# Handler for displaying logs dynamically
async def display_logs(request):
    html_content = "<h1>Logs</h1><ul>"
    for entry in logs:
        html_content += f"<li>{entry}</li>"
    html_content += "</ul>"
    return web.Response(text=html_content, content_type="text/html")

# Main setup for aiohttp server
app = web.Application()
app.add_routes([
    web.post('/log', log_data),
    web.post('/reset', reset_logs),
    web.get('/logs', display_logs),
])

if __name__ == '__main__':
    web.run_app(app, port=8080)
