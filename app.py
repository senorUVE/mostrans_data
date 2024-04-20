from flask import Flask, request, jsonify
import pandas as pd
import dateparser
import spacy
import logging
from itertools import chain, combinations
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


logging.basicConfig(filename='app.log', level=logging.DEBUG) #логирование

def all_combinations(any_list):
    iter = chain(*map(lambda x: combinations(any_list, x), range(0, 5)))
    comb = []
    for i in iter:
        comb.append(' '.join(list(i)))
    return comb

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data['text'].lower()

    df = pd.read_excel('/app/mostrans_data.xlsx')
    stations = df['Станция'].str.lower().values

    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)

    station_names = [ent.text for ent in doc.ents if ent.text in stations]
    dates = [dateparser.parse(word) for word in all_combinations(text.split()) if dateparser.parse(word)]

    return jsonify({'stations': station_names, 'dates': dates})
                    #.isoformat() for date in dates if date]})

if __name__ == '__main__':
    app.run(debug=True)
