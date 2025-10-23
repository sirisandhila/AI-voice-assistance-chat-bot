from flask import Flask, render_template, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class VoiceAssistantBackend:
    def __init__(self):
        self.jokes = [
            "Why did the programmer quit his job? Because he didn't get arrays! Get it? A raise!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "What's a programmer's favorite place? The foo bar!",
            "Why did the Python programmer not respond to messages? They were stuck in an infinite loop!"
        ]
        
        self.greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here to assist you."
        ]
    
    def get_response(self, user_input):
        """Generate response based on user input"""
        if not user_input:
            return "I didn't catch that. Could you repeat?"
        
        user_input = user_input.lower()
        
        # Greetings
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice(self.greetings)
        
        # How are you
        elif any(phrase in user_input for phrase in ['how are you', 'how do you do', 'how are things']):
            return "I'm doing great, thank you for asking! How are you?"
        
        # Name
        elif any(phrase in user_input for phrase in ['your name', 'who are you', 'what are you called']):
            return "I'm your Python voice assistant. You can call me VA!"
        
        # Time
        elif 'time' in user_input:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        
        # Date
        elif 'date' in user_input:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            return f"Today is {current_date}"
        
        # Capabilities
        elif any(phrase in user_input for phrase in ['what can you do', 'your capabilities', 'help']):
            return "I can tell you the time, date, answer simple questions, tell jokes, and have conversations with you. Just speak naturally!"
        
        # Joke
        elif 'joke' in user_input:
            return random.choice(self.jokes)
        
        # Weather (you can integrate a weather API here)
        elif 'weather' in user_input:
            return "I don't have access to weather data yet, but you can check your local weather forecast online!"
        
        # Exit commands
        elif any(word in user_input for word in ['bye', 'goodbye', 'exit', 'quit', 'stop']):
            return "Goodbye! Have a great day!"
        
        # Default response
        else:
            return "That's interesting! I'm still learning. Is there anything else I can help you with?"

# Initialize the assistant
assistant = VoiceAssistantBackend()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_speech():
    """Process speech input and return response"""
    try:
        data = request.get_json()
        user_input = data.get('text', '')
        
        response = assistant.get_response(user_input)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Voice Assistant Web Server Starting...")
    print("=" * 50)
    print("\n🌐 Open your browser and go to: http://localhost:5000")
    print("Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)