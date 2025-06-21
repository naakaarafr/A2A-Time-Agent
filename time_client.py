#!/usr/bin/env python3
"""
Terminal-based A2A (Agent-to-Agent) Client
This client can discover and communicate with A2A agents over HTTP.
"""

import requests
import uuid
import json
import sys
import argparse
from urllib.parse import urlparse, urljoin

class A2AClient:
    def __init__(self, agent_url):
        """Initialize the A2A client with an agent URL."""
        self.agent_url = agent_url.rstrip('/')
        self.agent_info = None
        
    def discover_agent(self):
        """
        Discover the agent by fetching its card from /.well-known/agent.json
        Returns True if successful, False otherwise.
        """
        discovery_url = f"{self.agent_url}/.well-known/agent.json"
        
        try:
            print(f"🔍 Discovering agent at: {discovery_url}")
            response = requests.get(discovery_url, timeout=10)
            
            if response.status_code == 200:
                self.agent_info = response.json()
                print(f"✅ Connected to: {self.agent_info.get('name', 'Unknown Agent')}")
                print(f"📝 Description: {self.agent_info.get('description', 'No description')}")
                print(f"🔧 Version: {self.agent_info.get('version', 'Unknown')}")
                
                capabilities = self.agent_info.get('capabilities', {})
                print(f"🎯 Capabilities:")
                print(f"   - Streaming: {capabilities.get('streaming', False)}")
                print(f"   - Push Notifications: {capabilities.get('pushNotifications', False)}")
                print()
                return True
            else:
                print(f"❌ Failed to discover agent: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error during discovery: {e}")
            return False
    
    def send_task(self, message_text):
        """
        Send a task to the agent using the A2A protocol.
        Returns the agent's response or None if failed.
        """
        if not self.agent_info:
            print("❌ Agent not discovered yet. Call discover_agent() first.")
            return None
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create A2A task payload
        task_payload = {
            "id": task_id,
            "message": {
                "role": "user",
                "parts": [{"text": message_text}]
            }
        }
        
        # Send task to agent
        task_url = f"{self.agent_url}/tasks/send"
        
        try:
            print(f"📤 Sending task: \"{message_text}\"")
            response = requests.post(task_url, json=task_payload, timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract agent's response from the messages
                messages = response_data.get("messages", [])
                if messages:
                    # Find the agent's response (last message with role "agent")
                    for msg in reversed(messages):
                        if msg.get("role") == "agent":
                            agent_reply = msg["parts"][0]["text"]
                            print(f"📥 Agent response: {agent_reply}")
                            return agent_reply
                
                print("⚠️  No agent response found in the task result")
                return None
                
            else:
                print(f"❌ Task failed: HTTP {response.status_code}")
                if response.text:
                    print(f"   Error details: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error during task: {e}")
            return None

def interactive_mode(client):
    """Run the client in interactive mode."""
    print("=== A2A Terminal Client - Interactive Mode ===")
    print("Type your messages to send to the agent")
    print("Commands: 'quit', 'exit', 'q' to leave, 'info' to show agent info")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            elif user_input.lower() == 'info':
                if client.agent_info:
                    print("🤖 Agent Information:")
                    print(json.dumps(client.agent_info, indent=2))
                else:
                    print("❌ No agent information available")
                continue
            
            elif user_input == '':
                continue
            
            else:
                # Send message to agent
                response = client.send_task(user_input)
                if not response:
                    print("⚠️  Failed to get response from agent")
            
            print()  # Add spacing between interactions
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def single_message_mode(client, message):
    """Send a single message and exit."""
    print("=== A2A Terminal Client - Single Message ===")
    response = client.send_task(message)
    if response:
        return 0  # Success
    else:
        return 1  # Failure

def main():
    parser = argparse.ArgumentParser(description="Terminal-based A2A Client")
    parser.add_argument('agent_url', help='URL of the A2A agent (e.g., http://localhost:5000)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--message', '-m', type=str,
                       help='Send a single message and exit')
    
    args = parser.parse_args()
    
    # Create client and discover agent
    client = A2AClient(args.agent_url)
    
    if not client.discover_agent():
        print("❌ Failed to connect to agent. Exiting.")
        return 1
    
    # Choose mode based on arguments
    if args.message:
        return single_message_mode(client, args.message)
    elif args.interactive:
        interactive_mode(client)
        return 0
    else:
        # Default: interactive mode
        interactive_mode(client)
        return 0

if __name__ == "__main__":
    sys.exit(main())