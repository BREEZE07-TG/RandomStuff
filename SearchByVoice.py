import asyncio
import aiohttp
import playsound
from gtts import gTTS
import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("🗣️ You said:", text)
        return text
    except sr.UnknownValueError:
        return "I couldn't understand your voice."
    except sr.RequestError as e:
        return f"Could not request results: {e}"


async def fetch_data(query):
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json"
        }
        url = "https://api.binjie.fun/api/generateStream"
        data = {
            "prompt": query,
            "network": True,
            "stream": False,
            "system": {
                "userId": "#/chat/1722576084617",
                "withoutContext": False
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                return await response.text()
    except Exception as e:
        return f"An error occurred: {str(e)}"


async def main():
   
    query = listen()

    
    print("🤖 Fetching AI response...")
    response = await fetch_data(query)
    
    
    print("🔊 Speaking response...")
    tts = gTTS(text=response[:1000], lang='en')
    tts.save("output.mp3")
    playsound.playsound("output.mp3")


asyncio.run(main())
