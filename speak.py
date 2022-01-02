import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 140)
engine.setProperty('voice', 'english')


def content(text, function):
    engine.connect("goal", function)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def default():
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)
    engine.say("You can do it")
    engine.runAndWait()
    engine.stop()
