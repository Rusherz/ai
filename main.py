import anago
import json

from anago.utils import load_data_and_labels

x_train, y_train = load_data_and_labels('./data.txt')
x_test, y_test = load_data_and_labels('./data/conll2003/en/ner/test.txt')

model = anago.Sequence().load(params_file='./params.h5', preprocessor_file='./pre.h5', weights_file='./weights.h5')
#model.fit(x_train, y_train, epochs=1)
#model.save(params_file='./params.h5', preprocessor_file='./pre.h5', weights_file='./weights.h5')

#print(model.score(x_test, y_test))

import re

text = re.sub('<[^<]+>', '', open('./168b2c68efa3c1d0c224ed2af8d845df.xml').read())

entities = model.analyze(text)
print(entities)
f = open('./results.json', 'w')
f.writelines(json.dumps(entities))
f.close()

