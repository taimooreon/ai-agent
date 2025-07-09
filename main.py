import openai
import speech_recognition as sr
import pyttsx3
import os

# 1. Set API Key securely
openai.api_key = "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"

# 2. Text-to-Speech Engine
tts_engine = pyttsx3.init()

# 3. Listen to user's voice
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"👤 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return None

# 4. Get GPT response using new SDK
def get_ai_response(user_input):
    print("🤖 Thinking...")
    client = openai.OpenAI(api_key="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")

    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = chat_completion.choices[0].message.content
    print(f"🤖 Agent: {reply}")
    return reply

# 5. Speak response
def speak_response(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# 6. Run main loop
if __name__ == "__main__":
    while True:
        user_input = listen_to_user()
        if user_input:
            ai_reply = get_ai_response(user_input)
            speak_response(ai_reply)
