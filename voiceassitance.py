import speech_recognition as sr # type: ignore
import pyttsx3 # pyright: ignore[reportMissingImports]
import datetime
import random

class VoiceAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        # Get available voices and set a voice
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Change index for different voices
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen to user's voice and convert to text"""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                audio = self.recognizer.listen(source, timeout=5)
                print("Recognizing...")
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Please try again.")
                return None
            
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't understand that. Could you repeat?")
                return None
            
            except sr.RequestError:
                self.speak("Sorry, there was an error with the speech recognition service.")
                return None
    
    def get_response(self, user_input):
        """Generate response based on user input"""
        
        if not user_input:
            return None
        
        # Greetings
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
            responses = [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! I'm here to assist you."
            ]
            return random.choice(responses)
        
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
            return "I can tell you the time, date, answer simple questions, and have a conversation with you. Just speak naturally!"
        
        # Joke
        elif 'joke' in user_input:
            jokes = [
                "Why did the programmer quit his job? Because he didn't get arrays! Get it? A raise!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "What's a programmer's favorite place? The foo bar!",
                "Why did the Python programmer not respond to messages? They were stuck in an infinite loop!"
            ]
            return random.choice(jokes)
        
        # Exit commands
        elif any(word in user_input for word in ['bye', 'goodbye', 'exit', 'quit', 'stop']):
            return "Goodbye! Have a great day!"
        
        # Default response
        else:
            return "That's interesting! I'm still learning. Is there anything else I can help you with?"
    
    def run(self):
        """Main loop to run the assistant"""
        self.speak("Hello! I'm your voice assistant. How can I help you today?")
        
        while True:
            # Listen to user
            user_input = self.listen()
            
            # Get response
            response = self.get_response(user_input)
            
            if response:
                self.speak(response)
                
                # Exit if goodbye
                if user_input and any(word in user_input for word in ['bye', 'goodbye', 'exit', 'quit', 'stop']):
                    break


def main():
    """Main function to start the voice assistant"""
    print("=" * 50)
    print("Python Voice Assistant")
    print("=" * 50)
    print("\nMake sure your microphone is connected and working!")
    print("Speak clearly after you hear 'Listening...'\n")
    
    assistant = VoiceAssistant()
    
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\n\nAssistant stopped by user.")
        assistant.speak("Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()