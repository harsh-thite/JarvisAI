import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import subprocess
import cohere
from config import apikey
import random

chatStr = ""

def chat(query):
    global chatStr
    co = cohere.Client(apikey)
    chatStr += f"Harsh: {query}\nJarvis: "

    # Create a completion request
    response = co.generate(
        model='command-r-plus',
        prompt=chatStr,
        max_tokens=256,
        temperature=0.7,
        p=1.0,  # Equivalent to top_p in OpenAI
        frequency_penalty=0,
        presence_penalty=0
    )

    # Wrap the response handling inside a try-catch block
    try:
        reply = response.generations[0].text
        print(reply)
        chatStr += f"{reply}\n"
        return reply
    except IndexError:
        return "No response generated."

def ai(prompt):
    co = cohere.Client(apikey)
    text = f"Cohere response for prompt: {prompt}\n**************************\n\n"

    # Create a completion request
    response = co.generate(
        model='command-r-plus',
        prompt=prompt,
        max_tokens=256,
        temperature=0.7,
        p=1.0,  # Equivalent to top_p in OpenAI
        frequency_penalty=0,
        presence_penalty=0
    )

    # Wrap the response handling inside a try-catch block
    try:
        reply = response.generations[0].text
        print(reply)
        text += reply
    except IndexError:
        text += "No response generated."

    if not os.path.exists("Cohere"):
        os.mkdir("Cohere")

    with open(f"Cohere/prompt-{random.randint(1, 2343434356)}.txt", "w") as f:
        f.write(text)

    return reply

def say(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 35)
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
        query = "Sorry, I did not get that"
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API service; {e}")
        query = "Sorry, there was an error with the speech service"
    return query

if __name__ == '__main__':
    print('PyCharm')
    say("Hey, it is Jarvis A I.")
    print("Yes, I am Listening...")
    while True:
        query = takeCommand()

        sites = [
            ["youtube", "https://www.youtube.com"],
            ["google", "https://www.google.com"],
            ["GCR", "https://www.classroom.google.com"],
            ["Chatgpt", "https://www.chatgpt.com"],
            ["LinkedIn", "https://www.linkedin.com"],
            ["github", "https://www.github.com"]
        ]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])

        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H:%M")
            minute = datetime.datetime.now().strftime("%M")
            say(f"The time is {hour} and {minute} minutes")

        if "Open Apple Music".lower() in query.lower():
            say("Opening Apple Music")
            applemusic_path = r"C:\Users\ASUS\AppData\Local\Microsoft\WindowsApps\AppleMusic.exe"
            if os.path.exists(applemusic_path):
                subprocess.Popen(applemusic_path)
            else:
                say("Apple Music is not installed at the expected location")

        if "Using Artificial Intelligence".lower() in query.lower():
            ai_response = ai(prompt=query)
            say(ai_response)

        # New addition for chatting with Jarvis
        if "" in query.lower() or "chat" in query.lower():
            chat_response = chat(query)
            say(chat_response)
