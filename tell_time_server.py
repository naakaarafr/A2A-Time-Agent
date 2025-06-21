#!/usr/bin/env python3
"""
A2A Time Agent Server (No Flask)
Implements the Agent-to-Agent protocol using Python's built-in HTTP server.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from datetime import datetime
import sys

class A2ATimeAgentHandler(BaseHTTPRequestHandler):
    """HTTP request handler that implements A2A protocol for a time agent."""
    
    def do_GET(self):
        """Handle HTTP GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/.well-known/agent.json":
            self.handle_agent_discovery()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle HTTP POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/tasks/send":
            self.handle_task()
        else:
            self.send_error(404, "Not Found")
    
    def handle_agent_discovery(self):
        """
        Handle A2A agent discovery endpoint: /.well-known/agent.json
        Returns agent metadata according to A2A specification.
        """
        agent_info = {
            "name": "TimeAgent",
            "description": "A helpful agent that tells you the current time when asked.",
            "url": f"http://localhost:{self.server.server_port}",
            "version": "1.0.0",
            "capabilities": {
                "streaming": False,
                "pushNotifications": False
            },
            "author": "Terminal A2A Demo",
            "tags": ["time", "utility", "demo"]
        }
        
        self.send_json_response(200, agent_info)
        print(f"🔍 Agent discovery request from {self.client_address[0]}")
    
    def handle_task(self):
        """
        Handle A2A task requests sent to /tasks/send
        Processes tasks according to A2A protocol specification.
        """
        try:
            # Read and parse the request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_json_response(400, {"error": "Empty request body"})
                return
            
            post_data = self.rfile.read(content_length)
            task = json.loads(post_data.decode('utf-8'))
            
            # Validate A2A task structure
            if not self.validate_task(task):
                self.send_json_response(400, {"error": "Invalid A2A task format"})
                return
            
            # Extract task information
            task_id = task["id"]
            user_message = task["message"]["parts"][0]["text"]
            
            print(f"📤 Received task from {self.client_address[0]}: \"{user_message}\"")
            
            # Process the task and generate response
            response_text = self.process_time_request(user_message)
            
            # Create A2A response
            response_data = {
                "id": task_id,
                "status": {"state": "completed"},
                "messages": [
                    task["message"],  # Echo back the original message
                    {
                        "role": "agent",
                        "parts": [{"text": response_text}]
                    }
                ]
            }
            
            self.send_json_response(200, response_data)
            print(f"📥 Sent response: \"{response_text}\"")
            
        except json.JSONDecodeError:
            self.send_json_response(400, {"error": "Invalid JSON in request body"})
        except Exception as e:
            print(f"❌ Error processing task: {e}")
            self.send_json_response(500, {"error": "Internal server error"})
    
    def validate_task(self, task):
        """Validate that the task follows A2A protocol format."""
        try:
            # Check required fields
            if "id" not in task:
                return False
            if "message" not in task:
                return False
            if "role" not in task["message"]:
                return False
            if "parts" not in task["message"]:
                return False
            if not isinstance(task["message"]["parts"], list):
                return False
            if len(task["message"]["parts"]) == 0:
                return False
            if "text" not in task["message"]["parts"][0]:
                return False
            
            return True
        except (KeyError, IndexError, TypeError):
            return False
    
    def process_time_request(self, user_message):
        """
        Process the user's message and generate an appropriate time response.
        This is where the agent's "intelligence" lives.
        """
        message_lower = user_message.lower()
        current_time = datetime.now()
        
        # Different responses based on what the user asked
        if any(word in message_lower for word in ['time', 'clock', 'hour', 'minute']):
            if 'date' in message_lower or 'today' in message_lower:
                return f"Today is {current_time.strftime('%A, %B %d, %Y')} and the current time is {current_time.strftime('%I:%M:%S %p')}"
            elif 'format' in message_lower or '24' in message_lower:
                return f"The current time in 24-hour format is: {current_time.strftime('%H:%M:%S')}"
            elif 'zone' in message_lower or 'timezone' in message_lower:
                return f"The current local time is: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            else:
                return f"The current time is: {current_time.strftime('%I:%M:%S %p')}"
        
        elif 'hello' in message_lower or 'hi' in message_lower:
            return f"Hello! The current time is {current_time.strftime('%I:%M:%S %p')}. How can I help you with time-related questions?"
        
        elif 'help' in message_lower:
            return "I'm a time agent! I can tell you the current time, date, or help with time-related questions. Just ask me 'What time is it?' or similar questions."
        
        else:
            # Default response - assume they want the time
            return f"I'm not sure exactly what you're asking, but the current time is: {current_time.strftime('%I:%M:%S %p')}"
    
    def send_json_response(self, status_code, data):
        """Send a JSON response with proper headers."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
        self.end_headers()
        
        response_json = json.dumps(data, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to provide cleaner logging."""
        # You can comment this out if you want detailed HTTP logs
        pass

def run_server(port=5000, host='localhost'):
    """Start the A2A Time Agent server."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, A2ATimeAgentHandler)
    httpd.server_port = port  # Store port for agent discovery URL
    
    print("🤖 A2A Time Agent Server Starting...")
    print(f"🌐 Server running at: http://{host}:{port}")
    print(f"🔍 Discovery endpoint: http://{host}:{port}/.well-known/agent.json")
    print(f"📤 Task endpoint: http://{host}:{port}/tasks/send")
    print("⌨️  Press Ctrl+C to stop the server")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        httpd.shutdown()
        print("👋 Server stopped.")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="A2A Time Agent Server")
    parser.add_argument('--port', '-p', type=int, default=5000,
                       help='Port to run the server on (default: 5000)')
    parser.add_argument('--host', type=str, default='localhost',
                       help='Host to bind the server to (default: localhost)')
    
    args = parser.parse_args()
    
    try:
        run_server(args.port, args.host)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {args.port} is already in use. Try a different port with --port")
        else:
            print(f"❌ Failed to start server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())