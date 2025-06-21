# A2A Time Agent

A lightweight Python implementation of the Agent-to-Agent (A2A) communication protocol, featuring a time server agent and terminal client for seamless agent communication.

## 🚀 Overview

The A2A Time Agent demonstrates how agents can discover and communicate with each other using standardized HTTP endpoints. This project includes:

- **Time Server Agent**: An A2A-compliant agent that provides time-related services
- **Terminal Client**: A command-line client for interacting with A2A agents
- **Protocol Implementation**: Full A2A specification support including agent discovery and task execution

## 🏗️ Architecture

### Agent-to-Agent Protocol
The A2A protocol enables agents to:
- **Discover** other agents via `/.well-known/agent.json` endpoints
- **Communicate** through structured JSON messages
- **Execute tasks** using standardized request/response patterns

### Components

**Time Server (`tell_time_server.py`)**
- Implements A2A protocol endpoints
- Provides intelligent time responses
- Supports multiple time formats and queries
- Built with Python's native HTTP server (no external dependencies)

**Terminal Client (`time_client.py`)**
- Discovers and connects to A2A agents
- Interactive and single-message modes
- Human-friendly command-line interface
- Works with any A2A-compliant agent

## 📦 Installation

### Prerequisites
- Python 3.6 or higher
- `requests` library for the client

### Setup
```bash
# Clone the repository
git clone https://github.com/naakaarafr/A2A-Time-Agent.git
cd A2A-Time-Agent

# Install client dependencies
pip install requests

# Make scripts executable (optional)
chmod +x tell_time_server.py time_client.py
```

## 🎯 Quick Start

### 1. Start the Time Agent Server
```bash
python tell_time_server.py
```

Default server runs on `http://localhost:5000`

**Custom port and host:**
```bash
python tell_time_server.py --port 8080 --host 0.0.0.0
```

### 2. Connect with the Terminal Client

**Interactive Mode:**
```bash
python time_client.py http://localhost:5000 --interactive
```

**Single Message:**
```bash
python time_client.py http://localhost:5000 --message "What time is it?"
```

## 🔧 Usage Examples

### Server Output
```
🤖 A2A Time Agent Server Starting...
🌐 Server running at: http://localhost:5000
🔍 Discovery endpoint: http://localhost:5000/.well-known/agent.json
📤 Task endpoint: http://localhost:5000/tasks/send
⌨️  Press Ctrl+C to stop the server

🔍 Agent discovery request from 127.0.0.1
📤 Received task from 127.0.0.1: "What time is it?"
📥 Sent response: "The current time is: 02:30:45 PM"
```

### Client Interaction
```
🔍 Discovering agent at: http://localhost:5000/.well-known/agent.json
✅ Connected to: TimeAgent
📝 Description: A helpful agent that tells you the current time when asked.
🔧 Version: 1.0.0
🎯 Capabilities:
   - Streaming: False
   - Push Notifications: False

=== A2A Terminal Client - Interactive Mode ===
Type your messages to send to the agent
Commands: 'quit', 'exit', 'q' to leave, 'info' to show agent info

You: What time is it?
📤 Sending task: "What time is it?"
📥 Agent response: The current time is: 02:30:45 PM

You: What's today's date?
📤 Sending task: "What's today's date?"
📥 Agent response: Today is Saturday, June 21, 2025 and the current time is 02:31:12 PM
```

## 🗣️ Supported Queries

The Time Agent understands various time-related requests:

| Query Type | Example | Response |
|------------|---------|----------|
| Basic Time | "What time is it?" | "The current time is: 02:30:45 PM" |
| Date & Time | "What's today's date?" | "Today is Saturday, June 21, 2025 and the current time is 02:30:45 PM" |
| 24-Hour Format | "Time in 24 hour format" | "The current time in 24-hour format is: 14:30:45" |
| Timezone | "Current time with timezone" | "The current local time is: 2025-06-21 14:30:45 EST" |
| Greeting | "Hello" | "Hello! The current time is 02:30:45 PM. How can I help you?" |
| Help | "Help" | "I'm a time agent! I can tell you the current time, date..." |

## 🌐 A2A Protocol Endpoints

### Agent Discovery: `GET /.well-known/agent.json`
Returns agent metadata:
```json
{
  "name": "TimeAgent",
  "description": "A helpful agent that tells you the current time when asked.",
  "url": "http://localhost:5000",
  "version": "1.0.0",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "author": "Terminal A2A Demo",
  "tags": ["time", "utility", "demo"]
}
```

### Task Execution: `POST /tasks/send`
Accepts A2A task format:
```json
{
  "id": "unique-task-id",
  "message": {
    "role": "user",
    "parts": [{"text": "What time is it?"}]
  }
}
```

Returns task result:
```json
{
  "id": "unique-task-id",
  "status": {"state": "completed"},
  "messages": [
    {
      "role": "user",
      "parts": [{"text": "What time is it?"}]
    },
    {
      "role": "agent",
      "parts": [{"text": "The current time is: 02:30:45 PM"}]
    }
  ]
}
```

## 🛠️ Command Line Options

### Server (`tell_time_server.py`)
```bash
python tell_time_server.py [options]

Options:
  --port, -p PORT    Port to run the server on (default: 5000)
  --host HOST        Host to bind the server to (default: localhost)
```

### Client (`time_client.py`)
```bash
python time_client.py AGENT_URL [options]

Arguments:
  AGENT_URL          URL of the A2A agent (e.g., http://localhost:5000)

Options:
  --interactive, -i  Run in interactive mode
  --message, -m MSG  Send a single message and exit
```

## 🔌 Extending the Project

### Creating New Agents
1. Implement the two required endpoints:
   - `GET /.well-known/agent.json` for discovery
   - `POST /tasks/send` for task execution

2. Follow the A2A message format for requests and responses

3. Add your custom logic in the task processing function

### Example: Weather Agent
```python
def process_weather_request(self, user_message):
    """Process weather-related requests"""
    if 'weather' in user_message.lower():
        return "Today's weather is sunny with 72°F"
    return "I can help you with weather information!"
```

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- **New Agent Types**: Calculator, translator, file server
- **Enhanced Protocol**: Streaming support, authentication
- **Better UX**: Web interface, configuration files
- **Testing**: Unit tests, integration tests
- **Documentation**: API docs, tutorials

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test them
4. Submit a pull request

## 📋 Requirements

### Server
- Python 3.6+
- No external dependencies (uses built-in libraries)

### Client
- Python 3.6+
- `requests` library

## 🐛 Troubleshooting

**Port Already in Use**
```bash
# Try a different port
python tell_time_server.py --port 8080
```

**Connection Refused**
- Ensure the server is running
- Check firewall settings
- Verify the correct URL and port

**Agent Not Found**
- Confirm the agent URL is correct
- Check that the agent implements `/.well-known/agent.json`

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Links

- **Repository**: https://github.com/naakaarafr/A2A-Time-Agent
- **Issues**: https://github.com/naakaarafr/A2A-Time-Agent/issues
- **A2A Protocol Specification**: [Learn more about Agent-to-Agent communication]

## 🙏 Acknowledgments

- Built following the Agent-to-Agent protocol specification
- Inspired by the need for simple, standardized agent communication
- Thanks to the open source community for Python libraries and tools

---

**Ready to build your own A2A agents? Start with this time agent and expand into a full agent ecosystem!** 🤖✨
