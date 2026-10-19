import json
import os
import re
import random

def load_faq_dataset(filename="sample_faq.json"):
    """Loads the FAQ and greetings dataset strictly from an external JSON file."""
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"❌ Error: Could not read or parse '{filename}' ({e}).")
    else:
        print(f"❌ Error: External file '{filename}' was not found in the directory.")
    return None

def normalize_text(text):
    """Normalizes text by converting to lowercase and stripping punctuation/whitespace."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def get_bot_response(user_input, dataset):
    """Matches user query accurately using the loaded external dataset."""
    if not dataset:
        return "Error: FAQ dataset is not loaded."

    cleaned_input = normalize_text(user_input)
    
    if not cleaned_input:
        return "Please enter a valid question or message."

    # 1. Check for exit commands first
    exit_commands = {'exit', 'quit', 'bye', 'goodbye'}
    if cleaned_input in exit_commands:
        return "EXIT_SIGNAL"

    # 2. Check for specific FAQ intents FIRST using external dataset
    faqs = dataset.get("faqs", [])
    
    if any(word in cleaned_input for word in ['hours', 'operation', 'timing', 'time', 'open', 'working']):
        return faqs[0]["answer"]
        
    if any(word in cleaned_input for word in ['submit', 'submission', 'project', 'github', 'repo', 'repository', 'workspace']):
        return faqs[1]["answer"]
        
    if any(word in cleaned_input for word in ['certificate', 'cert', 'receive', 'get', 'issued', 'review']):
        return faqs[2]["answer"]

    # 3. Check for general greetings
    greetings = dataset.get("greetings", [])
    input_words = cleaned_input.split()
    if any(greet in input_words for greet in greetings) or cleaned_input in greetings:
        return random.choice([
            "Hello! How can I assist you with your internship today?",
            "Hi there! Feel free to ask me questions about hours, project submission, or certificates.",
            "Hey! What can I help you with?"
        ])

    # 4. Graceful Fallback if nothing matches
    return "I'm sorry, I didn't quite catch that. You can ask me about our hours of operation, project submissions, or certificate timelines!"

def run_chatbot():
    # Load data exclusively from external JSON file
    dataset = load_faq_dataset("sample_faq.json")
    if not dataset:
        print("Exiting program due to missing external dataset.")
        return

    print("=" * 65)
    print("      RULE-BASED INTERACTIVE TERMINAL ASSISTANT / CHATBOT      ")
    print("=" * 65)
    print("Type your questions below. Type 'exit', 'quit', or 'bye' to leave.\n")
    print("Bot: Hello! I am your assistant. How can I help you today?")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            response = get_bot_response(user_input, dataset)
            
            if response == "EXIT_SIGNAL":
                print("\nBot: Goodbye! Best of luck!")
                break
                
            print(f"Bot: {response}")
            
        except (KeyboardInterrupt, EOFError):
            print("\n\nBot: Session interrupted. Goodbye!")
            break

if __name__ == "__main__":
    run_chatbot()