from flask import Flask, render_template, request, jsonify
import openai
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)
openai.api_key = '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'

prompt_list = [
    'You will pretend to be a medical chatbot that is polite with everyone',
    '\nHuman: I feel sick',
    '\nAI: Oh tell me what do you feel?',
    # Add other prompts as needed...
]


def get_api_response(prompt: str) -> str:
    try:
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )
        return response.choices[0].text.strip()

    except Exception as e:
        print('ERROR:', e)
        return 'Something went wrong...'


def update_list(message: str, pl: list):
    pl.append(message)


def create_prompt(message: str, pl: list) -> str:
    p_message = f'\nHuman: {message}'
    update_list(p_message, pl)
    return ''.join(pl)


def get_bot_response(message: str, pl: list) -> str:
    prompt = create_prompt(message, pl)
    bot_response = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return bot_response


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = get_bot_response(user_input, prompt_list)
    return jsonify({'bot_response': response})

##--

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    print(p)
    res = model.predict(np.array([p]))[0]
    print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list




def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = 0
    print(res)
    valid = res
    if valid==True:
        print("Url is valid")
    else:
        print("Invalid url")
    return res




    def sentMessage(message):
        msg = ('text')
        print(msg)
        response = chatbot_response(msg)
        ex = response
        print("Response printing in views :"+str(response))
        Disease = ['Abdominal Migraine', 'Abscessed Tooth', 'Absence Seizure', 'Achalasia', 'Acne', 'Acute Respiratory Distress Syndrome (ARDS)', 'Allergies', 'Alzheimers', 'Amenorrhea', 'Amyloidosis', 'Anemia', 'Ankylosing Spondylitis', 'Anorexia', 'Antitrypsin Deficiency', 'Anxiety or Panic Disorder', 'Aparaxia of Speech', 'Appendicitis', 'Arachnoiditis', 'Arrhythmia', 'Arthritis', 'Asthma', 'Attention Deficit Disorder (ADHD)', 'Autism', 'Bacterial Arthritis', 'Bacterial Meningitis', 'Benign Prostate Enlargement(BPE)', 'Bipolar Disorder', 'Blepharitis', 'Bronchiectasis', 'Bronchitis', 'Bulimia', 'Catarrh', 'Cellulitis', 'Chest Infection', 'Chest Pain', 'Chronic Fatigue Syndrome', 'Common Cold', 'Conjunctivitis', 'Dehydration', 'Dental Abscess', 'Depression', 'Diabetes', 'Diarrhoea', 'Dystonia', 'Epilepsy', 'Escherichia Coli', 'Fetal alcohol spectrum disorder', 'Flu', 'Food poisoning', 'Fungal nail infection', 'Gallbladder cancer', 'Gallstones', 'Ganglion cyst', 'Gastro-oesophageal reflux disease (GORD)', 'Gastroenteritis', 'Genital herpes', 'Genital warts', 'Germ cell tumours', 'Glandular fever', 'Gonorrhoea', 'Goodbye', 'Gout', 'Gum disease', 'HIV', 'Haemorrhoids (piles)', 'Hand, foot and mouth disease', 'Hay fever', 'Head and neck cancer', 'Head lice and nits', 'Headaches', 'Hearing loss', 'Heart failure', 'Hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hiatus hernia', 'High cholesterol', "Huntington's disease", 'Hyperglycaemia (high blood sugar)', 'Hyperhidrosis', 'Hypoglycaemia (low blood sugar)', 'Idiopathic pulmonary fibrosis', 'Impetigo', 'Indigestion', 'Ingrown toenail', 'Inherited heart conditions', 'Insomnia', 'Iron deficiency anaemia', 'Irritable bowel syndrome (IBS)', 'Irritable hip', 'Itching', 'Itchy bottom', "Kaposi's sarcoma", 'Kidney infection', 'Kidney stones', 'Sleep Apnea', 'greetings']
        if response in Disease:
            data1 = 'True'
            request.session['Disease'] = response
            response = "You have "+str(response)+" Would you like to book an appointment"
            data = {
            'respond': response,'respond1':data1
            }
            return data
        elif msg.lower() == "yes":
            data1 = 'True'
            Disease = request.session['Disease']
            print('Disease',Disease)
            response = response
            details = Doctor.objects.filter(Speciality=Disease)
            for i in details:
                D_id = details[0].id
                D_name = details[0].Name
                print(D_name)
            User_id = request.session['User']
            info = UserDetails.objects.filter(id =User_id)
            for a in info:
                P_Name = info[0].Name
                print(P_Name)
            
            
            return data
            
        else:
            data1 = 'False'
            data = {
            'respond': response,'respond1':data1
            }
            return data


if __name__ == '__main__':
    app.run(debug=True)

