import spacy
from spacy.pipeline.textcat import DEFAULT_CONFIG

print("spaCy version", spacy.__version__)

nlp = spacy.blank('en')
print("initial pipes", nlp.pipe_names)

try:
    textcat = nlp.add_pipe('textcat', config={'exclusive_classes': True, 'architecture': 'simple_cnn'})
    print('added textcat', textcat)
except Exception as e:
    print('error adding textcat:', type(e), e)

print('default textcat config', DEFAULT_CONFIG)
