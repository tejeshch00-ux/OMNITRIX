import os
import sys
import time
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
from langdetect import detect
import pygame
from google import genai
from google.genai import types

# ==========================================
# 1. SECURE CONFIGURATION & INITIALIZATION
# ==========================================
# Load the secret environment variables from the hidden .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Safety Check: Verify the script successfully found your hidden key
if not API_KEY:
    print("\n[ CRITICAL ERROR: API KEY NOT DETECTED ]")
    print("Ensure you created a file named exactly '.env' in your OMNITRIX folder.")
    print("Inside it, you must have: GEMINI_API_KEY=your_actual_key_here")
    sys.exit()

try:
    # Initialize the Google GenAI Client securely using the hidden environment variable
    client = genai.Client(api_key=API_KEY)
    
    SYSTEM_INSTRUCTION = (
        "You are Omnitrix, an advanced AI assistant. "
        "Speak to the user like a real person—highly intelligent, professional, and natural. "
        "Keep your responses concise and easy to understand when spoken aloud. "
        "You are truly multilingual. You are free to respond in English, Telugu, Hindi, or "
        "any other language requested by the user. Always address the user as 'sir'."
    )
    
    # Open stateful chat link
    omnitrix_chat = client.chats.create(
        model='gemini-2.5-flash-lite',
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )
    print("--- Omnitrix: Secure Cloud Voice Systems Online ---")

except Exception as e:
    print(f"CRITICAL INITIALIZATION ERROR: {e}")
    sys.exit()

# ==========================================
# 2. UNIVERSAL CLOUD VOICE ENGINE
# ==========================================
def omnitrix_speak(text):
    print(f"Omnitrix: {text}")
    temp_filename = "omnitrix_speech.mp3"
    try:
        # Dynamic Global Language Detector
        try:
            voice_lang = detect(text)  # Automatically extracts language codes
        except Exception:
            voice_lang = 'en'  # Fallback accent
        
        # Request speech file from Google Cloud TTS using the auto-detected language
        tts = gTTS(text=text, lang=voice_lang, slow=False)
        tts.save(temp_filename)
        
        # Stream audio via Pygame audio layer
        pygame.mixer.init()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        
        # Hold execution until the audio finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        
        # Safe cleanup of local cache file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
    except Exception as e:
        print(f"Voice Output Error: {e}")
        try:
            pygame.mixer.quit()
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        except:
            pass

# ==========================================
# 3. AUDIO RECOGNITION (Microphone Input)
# ==========================================
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("[ Listening... Speak now, sir ]")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            return r.recognize_google(audio)
        except Exception:
            print("[ Microphone timed out or heard nothing ]")
            return None

# ==========================================
# 4. MAIN PROGRAM LOOP
# ==========================================
if __name__ == "__main__":
    omnitrix_speak("Omnitrix secure vocal link established, sir.")
    
    while True:
        print("\n--------------------------------------------------")
        user_input = input("You (Type a message, or press ENTER to use voice): ").strip()
        
        user_say = None
        if user_input:
            user_say = user_input
        else:
            user_say = get_audio()
            if user_say:
                print(f"You (Voice): {user_say}")
        
        if user_say and len(user_say.strip()) > 1:
            if "shut down" in user_say.lower() or "power off" in user_say.lower():
                omnitrix_speak("Powering down system links. Goodbye, sir.")
                break
            
            try:
                response = omnitrix_chat.send_message(user_say)
                if response.text:
                    omnitrix_speak(response.text)
                    time.sleep(2) # Protective cooldown spacer
                
            except Exception as e:
                print(f"\n[ RAW SERVER ERROR -> {e} ]") 
                if "429" in str(e) or "quota" in str(e).lower():
                    omnitrix_speak("Neural network recharging. Cooldown activated.")
                    time.sleep(60) 
                elif "503" in str(e) or "unavailable" in str(e).lower():
                    omnitrix_speak("Google servers are experiencing high traffic, sir. Retrying in ten seconds.")
                    time.sleep(10)
                else:
                    time.sleep(5)
        else:
            time.sleep(0.5)