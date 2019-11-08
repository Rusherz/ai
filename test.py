import os
import argparse, sys

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

parser=argparse.ArgumentParser()

parser.add_argument('--cpus', help='Number of cpus')
parser.add_argument('--iterations', help='Number of iterations')
parser.add_argument('--data_points', help='Number of rows to return')
parser.add_argument('--drop_out', help='Drop out rate, makes it harder for the model to remember')

args = parser.parse_args()

if args.cpus is not None:
    process_count = int(args.cpus)
else:
    process_count = 1

if args.data_points is not None:
    limit = int(args.data_points)
else:
    limit = 1000

if args.drop_out is not None:
    drop_out = float32(args.drop_out)
else:
    drop_out = 0.2

if args.iterations is not None:
    iterations = int(args.iterations)
else:
    iterations = 1

annotations = session.query(Annotation).limit(limit).all()

TRAIN_DATA = []

if os.path.isdir('./model'):
    nlp = spacy.load('./model')
else:
    nlp = spacy.blank('en')  # create blank Language class

optimizer = []

for annotation in annotations:
    document = 'DOI: ' + annotation.document
    TRAIN_DATA.append((
        document, {
            'entities': [
                (
                    int(annotation.start) + 5,
                    int(annotation.end) + 5,
                    annotation.entity
                )
            ]
        }
    ))

def train_spacy():
    global nlp

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe('ner')


    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()

        for iteration in range(iterations):
            pool = multiprocessing.Pool(processes=process_count)
            split_training = []
            max_length = (len(TRAIN_DATA) / process_count)

            for i in range(process_count):
                start = 0
                end = max_length

                if i != 0:
                    start = int((i - 1) * max_length)
                    end = int(i * max_length)
                else:
                    # Got nothing to do here, proper start and end are already set
                    pass

                if (i * max_length) > len(TRAIN_DATA):
                    end = len(TRAIN_DATA)

                print(str(start), str(end))
                split_training.append((TRAIN_DATA[int(start):int(end)], optimizer, iteration))

            print('iteration: ', str(iteration))
            results = pool.map(update_spacy, split_training)
            pool.close()
            pool.join()

    return nlp

def update_spacy(data):
    data_set = data[0]
    optimizer = data[1]

    print("Statring iteration " + str(data[2]))
    random.shuffle(data_set)
    losses = {}
    for text, annotations in data_set:
        nlp.update(
            [text],  # batch of texts
            [annotations],  # batch of annotations
            drop=drop_out,  # dropout - make it harder to memorise data
            sgd=optimizer,  # callable to update weights
            losses=losses)

    print(losses)

prdnlp = train_spacy()

# Save our trained Model
prdnlp.to_disk('./model')

#Test your text
test_text = input("Enter your testing text: ")
doc = prdnlp(test_text)
for ent in doc.ents:
    print(ent.text, len(ent.text), ent.start_char, ent.end_char, ent.label_)
