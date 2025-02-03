#third time IS the charm 
import pyttsx3
import time
import string
from RealtimeSTT import AudioToTextRecorder
from nav_classifier import RoomClassifier

classifier = RoomClassifier()
engine = pyttsx3.init()


def clean_text(text):
    cleaned_text = text.strip().lower()
    cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation))
    print(f"User: '{cleaned_text}'")    
    return cleaned_text  

def wake_word(text):
    if text:
        cleaned_text = clean_text(text)
        if "hey tori" in cleaned_text or "hey tory" in cleaned_text:
            engine.say("Hi, I'm Tori, a tour guide robot in Unity Hall. Would you like to say a navigation command or ask me a question?")
            engine.runAndWait()
            time.sleep(0.5)
            return True
    return False

def handle_navigation(recorder, classifier):
    engine.say("Where do you want to go?")
    engine.runAndWait()
    time.sleep(1)
    
    attempts = 0
    MAX_ATTEMPTS = 3
    
    while attempts < MAX_ATTEMPTS:
        text = recorder.text()
        if exit(text):
            return None
            
        if text:
            cleaned_text = clean_text(text)
            response = classifier.get_navigation_response(cleaned_text)
            
            if response['success']:
                engine.say(response['message'])
                engine.runAndWait()
                print("Location info:", classifier.extract_location_info(cleaned_text))
                return True
            
            attempts += 1
            if attempts < MAX_ATTEMPTS:
                if response['missing'] == 'both':
                    prompt = "I need both a room and floor. Please specify where you want to go."
                elif response['missing'] == 'room':
                    prompt = "Which room are you looking for?"
                elif response['missing'] == 'floor':
                    prompt = "Which floor is that on?"
                else:
                    prompt = "I didn't understand. Please try again."
                
                engine.say(prompt)
                engine.runAndWait()
            else:
                engine.say("I'm still having trouble understanding. Let's start over. Please say the wake phrase when you're ready.")
                engine.runAndWait()
                classifier.reset_context() #reset context for next run 
                return False 
    return False

def question(): 
    print("Ask question")
    return True

def exit(text): 
    if text:
        cleaned_text = clean_text(text)
        exit_words = {"stop", "goodbye", "bye"}
        if any(word in cleaned_text.lower() for word in exit_words):
            engine.say("Goodbye!")
            engine.runAndWait()
            return True
    return False

def main(): 
    recorder = AudioToTextRecorder()
    classifier = RoomClassifier()
    
    try:
        while True:
            print("Listening for the wake phrase...")
            
            while True:  # wake word loop
                text = recorder.text()
                if exit(text):
                    return
                if wake_word(text):
                    break
            
            while True: #command loop 
                text = recorder.text()
                if exit(text):
                    return
                if text:
                    cleaned_text = clean_text(text)
                    if "navigation command" in cleaned_text:
                        nav_result = handle_navigation(recorder, classifier)
                        if exit(text):
                            return
                        if nav_result:  # successful navigation 
                            print("insert nav stack code")
                            classifier.reset_context()  # reset context after navigation
                            return
                        if not nav_result:  # restart after 3 attempts
                            break 
                    elif "question" in cleaned_text:
                        question()
                        break
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

if __name__ == "__main__":
    main()

#what if user wants to go to its current location? Does this need to be a case in the code in case Tori is already at localized location? 