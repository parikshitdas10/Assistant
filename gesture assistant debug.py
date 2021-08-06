import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import cv2
import numpy as np
import math
import time

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

    speak("I am GOVI, a gesture operated virtual assistant")
    speak("show one finger to open google")
    speak("show two fingers to open facebook")
    speak("show 3 fingers to know the time")
    speak("show 4 fingers to turn me off")


# code for gesture control
def gesture():
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        # read image
        ret, img = cap.read()

        # get hand data from the rectangle sub window on the screen
        cv2.rectangle(img, (300, 300), (100, 100), (0, 255, 0), 0)
        crop_img = img[100:300, 100:300]

        # convert to grayscale
        grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # applying gaussian blur
        value = (35, 35)
        blurred = cv2.GaussianBlur(grey, value, 0)

        # thresholdin: Otsu's Binarization method
        _, thresh1 = cv2.threshold(
            blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        # show thresholded image
        #cv2.imshow('Thresholded', thresh1)

        # check OpenCV version to avoid unpacking error
        (version, _, _) = cv2.__version__.split('.')

        if version == '3':
            image, contours, hierarchy = cv2.findContours(thresh1.copy(),
                                                          cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        elif version == '4':
            contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_NONE)

        # find contour with max area
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

        # create bounding rectangle around the contour (can skip below two lines)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)

        # finding convex hull
        hull = cv2.convexHull(cnt)

        # drawing contours
        drawing = np.zeros(crop_img.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)

        # finding convex hull
        hull = cv2.convexHull(cnt, returnPoints=False)

        # finding convexity defects
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

        # applying Cosine Rule to find angle for all defects (between fingers)
        # with angle > 90 degrees and ignore defects
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]

            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

            # ignore angles > 90 and highlight rest with red dots
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
            #dist = cv2.pointPolygonTest(cnt,far,True)

            # draw a line from start to end i.e. the convex points (finger tips)
            # (can skip this part)
            cv2.line(crop_img, start, end, [0, 255, 0], 2)
            # cv2.circle(crop_img,far,5,[0,0,255],-1)

        # define actions required
        if count_defects == 1:
            c2 = c2+1
        elif count_defects == 0:
            c1 = c1+1
        elif count_defects == 2:
            c3 = c3+1
        elif count_defects == 3:
            c4 = c4+1
        # show appropriate images in windows
        #cv2.imshow('Gesture', img)
        all_img = np.hstack((drawing, crop_img))
        cv2.imshow('Contours', all_img)
        k = cv2.waitKey(10)
        if c1 > 80 or c2 > 80 or c3 > 80:
            break
    time.sleep(5)
    if c1 > 80:
        return "open google"
    elif c2 > 80:
        return "open facebook"
    elif c3 > 80:
        return "tell time"
    elif c4 > 80:
        return "close"


def takeCommand():
    try:
        print("Recognizing...")
        # Using google for voice recognition.
        query = gesture()
        print(f"User said: {query}\n")  # User query will be printed.

    except Exception as e:
        # print(e)
        # Say that again will be printed in case of improper voice
        speak("Sorry i couldn't understand")
        print("Sorry I couldn't understand")
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
            speak("opening google")
            webbrowser.open("google.com")
        elif 'facebook' in query:
            speak("I'm opening facebook")
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
