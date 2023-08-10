import openai
import pyttsx3 # text-to-spech

########### PYTTSX3 ###########
engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 1)

########### OPEN AI | CHAT-GPT3 ###########
apikey = YOUR_API_KEY
openai.api_key = apikey
gpt_model = 'gpt-3.5-turbo' # trained model

def play(text):
    engine.say(text)
    engine.runAndWait() #time delay for speak

def askGPT(promt):
    result = openai.ChatCompletion.create(model=gpt_model,
                                    messages=[{'role': 'assistant','content': promt}])
    answer = result.choices[0].message.content
    print('Answer:', answer)

    ########### SPECH ANSWER ###########
    play(answer)
