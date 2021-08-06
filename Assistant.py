import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser


engine = pyttsx3.init('sapi5')

voice = engine.getProperty('voices')  # getting details of current voice

engine.setProperty('voice', voice[0].id)


def speak(audio):

    engine.say(audio)

    engine.runAndWait()


def wishme():

    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am AAVAI, please dont waste my time and tell me what to do already!")


def takeCommand():
    # for terminal use
    #query = input("type it here: ")
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        r.energy_threshold = 0
        r.adjust_for_ambient_noise(source=source)
        audio = r.listen(source, timeout=3)

    try:
        print("Recognizing...")
        # Using google for voice recognition.
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")  # User query will be printed.

    except Exception as e:
        # print(e)
        # Say that again will be printed in case of improper voice
        speak("Can you try speaking properly?")
        print("Can you try speaking properly?")
        return "None"
    return query

    


if __name__ == "__main__":

    speak("Hi Parikshit")
    wishme()
    while True:
        # if 1:
        query = takeCommand().lower()  # Converting user query into lower case

        # Logic for executing tasks based on query
        if 'wikipedia' in query:  # if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'youtube' in query:
            speak("you know, you could have done that yourself!")
            speak("Anyway, I'm opening youtube!")
            webbrowser.open("youtube.com")
        elif 'google' in query:
            webbrowser.open("google.com")
        elif 'facebook' in query:
            speak("How about you try studying")
            speak("Anyway I'm opening facebook")
            webbrowser.open("facebook.com")
        elif 'instagram' in query:
            webbrowser.open("instagram.com")
        elif 'hello' in query:
            speak(
                "Hi there, Just tell me what task you want me to perform, I'm not your friend!")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"The time is {strTime}")
        elif 'close' in query:
            speak("Sigh! What a tiring day!")
            break
