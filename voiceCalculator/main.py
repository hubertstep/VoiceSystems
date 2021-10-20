# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import random
import time
import speech_recognition as sr

import random
import time
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language="pl-PL")
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":

    equations = ['plus', 'dodać', 'minus', 'odjąć', 'podzielić na', 'Podziel', 'podzielić przez', 'razy',
                 'pomnożone przez', 'x', 'potęga', 'silnia', 'pierwiastek']
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    instructions = (
        "Hello there! I am your calculator :) What would you like to do?\n"
    )

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(3)

    for j in range(PROMPT_LIMIT):
        print('Speak!')
        guess = recognize_speech_from_mic(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        print("I didn't catch that. What did you say?\n")

    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))

    print("Działanie:", guess["transcription"])

    res = ''.join([i for i in guess["transcription"] if not i.isdigit()])
    res = ''.join([i for i in res if not i == ' '])
    if res not in equations:
        print("nieznane działanie: ", res)

    a_list = ''.join([i for i in guess["transcription"] if i.isdigit()])
    map_object = map(int, a_list)
    list_of_integers = list(map_object)
    print(list_of_integers)

    if res == equations[0] or res == equations[1]:
        print("Dodaję")
        solution = list_of_integers[0] + list_of_integers[1]
    if res == equations[2] or res == equations[3]:
        print('Odejmuję')
        solution = list_of_integers[0] - list_of_integers[1]
    if res == equations[4] or res == equations[5] or res == equations[6]:
        print("Dzielę")
        if list_of_integers[1] != 0:
            solution = list_of_integers[0] / list_of_integers[1]
        else:
            print('Nie można dzielić przez 0!')
    if res == equations[7] or res == equations[8] or res == equations[9]:
        print("Mnożę")
        solution = list_of_integers[0] * list_of_integers[1]
    if res ==equations[10]:
        solution = math.pow(list_of_integers[0], list_of_integers[1])
    if res == equations[11]:
        solution = math.factorial(list_of_integers[0])
    if res == equations[12]:
        solution = math.sqrt(list_of_integers[0])

    print("Wynik działania: ", guess["transcription"], " to ", solution)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
