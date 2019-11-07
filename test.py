import spacy
import random
import multiprocessing

import sqlalchemy as db

from models.Annotation import Annotation

# From SQL Alchemy, import useful functions and classes that
# are for use within the configuration and instantiation of our database.
from sqlalchemy.orm import sessionmaker

# Our engine will act as our connector. This needs to persist for the duration of our
# script, whether exected with a completion, or left running indefinitely.
Engine = db.create_engine(
    'mysql+pymysql://server:^C{WZwVa4&kvxhd\'@jmir-mysql-production.cmlc7celvj8o.us-east-2.rds.amazonaws.com:3306/jmir-ml?charset=utf8')

# A factory for our connection is made available for us through the session maker.
Session = sessionmaker(bind=Engine)

# Creating an instance of our session via our factory.
session = Session()

annotations = session.query(Annotation).limit(1000).all()

TRAIN_DATA = []

nlp = spacy.blank('en')  # create blank Language class

optimizer = []

for annotation in annotations:
    TRAIN_DATA.append((
        annotation.document, {
            'entities': [
                (
                    annotation.start,
                    annotation.end,
                    annotation.entity
                )
            ]
        }
    ))

def train_spacy(iterations):
    global nlp

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)


    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()

        pool = multiprocessing.Pool(processes=4)
        split_iterations = []

        for i in range(4):
            split_iterations.append((int(iterations / 4), optimizer))

        print(split_iterations)
        results = pool.map(update_spacy, split_iterations)
        pool.close()
        pool.join()

    return nlp

def update_spacy(data):
    optimizer = data[1]

    for itn in range(data[0]):
        print("Statring iteration " + str(itn))
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            nlp.update(
                [text],  # batch of texts
                [annotations],  # batch of annotations
                drop=0.2,  # dropout - make it harder to memorise data
                sgd=optimizer,  # callable to update weights
                losses=losses)
        print(losses)

prdnlp = train_spacy(20)

# Save our trained Model
modelfile = input("Enter your Model Name: ")
prdnlp.to_disk(modelfile)

#Test your text
test_text = input("Enter your testing text: ")
doc = prdnlp(test_text)
for ent in doc.ents:
    print(ent.text, len(ent.text), ent.start_char, ent.end_char, ent.label_)
