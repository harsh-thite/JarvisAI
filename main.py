import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import subprocess
import cohere
import smtplib
import requests
from config import apikey, weather_api_key, email_user, email_pass
import random

chatStr = ""

def chat(query):
    global chatStr
    co = cohere.Client(apikey)
    chatStr += f"Harsh: {query}\nIntraAI: "

    response = co.generate(
        model='command-r-plus',
        prompt=chatStr,
        max_tokens=256,
        temperature=0.7,
        p=1.0,  # Equivalent to top_p in OpenAI
        frequency_penalty=0,
        presence_penalty=0
    )

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

    response = co.generate(
        model='command-r-plus',
        prompt=prompt,
        max_tokens=256,
        temperature=0.7,
        p=1.0,  # Equivalent to top_p in OpenAI
        frequency_penalty=0,
        presence_penalty=0
    )

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

# New Feature: Weather Report
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        res = requests.get(url)
        data = res.json()
        if data["cod"] != "404":
            weather = data["main"]
            temperature = weather["temp"]
            say(f"The temperature in {city} is {temperature} degrees Celsius")
        else:
            say("City not found")
    except Exception as e:
        say(f"Failed to get weather: {e}")

# New Feature: Send Email
def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(email_user, to, content)
        server.close()
        say("Email has been sent!")
    except Exception as e:
        say(f"Failed to send email: {e}")

if __name__ == '__main__':
    print('PyCharm')
    say("Hey, it is IntraAI.")
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

        if "artificial intelligence" in query.lower():
            ai_response = ai(prompt=query)
            say(ai_response)

        if "weather in" in query.lower():
            city = query.split("in")[-1].strip()
            get_weather(city)

        if "email to" in query.lower():
            try:
                say("What should I say?")
                content = takeCommand()
                to = query.split("to")[-1].strip() + "@gmail.com"
                send_email(to, content)
            except Exception as e:
                say(f"Sorry, I couldn't send the email due to: {e}")
