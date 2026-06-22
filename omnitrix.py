import speech_recognition as sr
from gtts import gTTS
from langdetect import detect
import pygame
from google import genai
from google.genai import types
import time
import sys
import os

# ==========================================
# 1. CORE CONFIGURATION & AI INITIALIZATION
# ==========================================
API_KEY = "" 

try:
    # Initialize the modern Google GenAI Client
    client = genai.Client(api_key=API_KEY)
    
    SYSTEM_INSTRUCTION = (
        "You are Omnitrix, an advanced AI assistant. "
        "Speak to the user like a real person—highly intelligent, professional, and natural. "
        "Keep your responses concise and easy to understand when spoken aloud. "
        "You are truly multilingual. You are free to respond in English, Telugu, Hindi, or "
        "any other language requested by the user. Always address the user as 'sir'."
    )
    
    # Open stateful chat link using the optimized Flash-Lite model
    omnitrix_chat = client.chats.create(
        model='gemini-2.5-flash-lite',
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )
    print("--- Omnitrix: Universal Cloud Voice Systems Online ---")

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
            voice_lang = detect(text)  # Automatically extracts codes (e.g., 'te', 'en', 'hi', 'fr')
        except Exception:
            voice_lang = 'en'  # Standard fallback if text contains only emojis or symbols
        
        # Request speech file from Google Cloud TTS using the auto-detected language
        tts = gTTS(text=text, lang=voice_lang, slow=False)
        tts.save(temp_filename)
        
        # Stream audio via Pygame audio layer
        pygame.mixer.init()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        
        # Hold the thread execution until the voice finishes speaking
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        
        # Safe cleanup of local cache file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
    except Exception as e:
        print(f"Voice Output Error: {e}")
        # Secondary safety cleanup sequence in case of failure mid-playback
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
        # Background noise filter sequence
        r.adjust_for_ambient_noise(source, duration=1)
        print("[ Listening... Speak now, sir ]")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            return r.recognize_google(audio)
        except Exception:
            print("[ Microphone timed out or heard nothing ]")
            return None

# ==========================================
# 4. EXECUTABLE APPARATUS LOOP
# ==========================================
if __name__ == "__main__":
    omnitrix_speak("Omnitrix vocal link established, sir.")
    
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
            # Command override shutdown sequence
            if "shut down" in user_say.lower() or "power off" in user_say.lower():
                omnitrix_speak("Powering down system links. Goodbye, sir.")
                break
            
            try:
                # Transmit dialogue turn to Gemini Cloud
                response = omnitrix_chat.send_message(user_say)
                if response.text:
                    omnitrix_speak(response.text)
                    time.sleep(2) # Protective cooldown spacer for metrics stability
                
            except Exception as e:
                print(f"\n[ RAW SERVER ERROR -> {e} ]") 
                # Intelligent defensive rate limit handler
                if "429" in str(e) or "quota" in str(e).lower():
                    omnitrix_speak("Neural network recharging. Cooldown activated.")
                    time.sleep(60) 
                else:
                    time.sleep(5)
        else:
            time.sleep(0.5)