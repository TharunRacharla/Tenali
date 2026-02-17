import json
import random
import spacy
from spacy.util import minibatch, compounding
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INTENT_FILE = BASE_DIR / 'data' / 'Intent.json'
MODEL_DIR = BASE_DIR.parent / 'nlu_model'


def load_intent_data(path=INTENT_FILE):
    with open(path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    texts = []
    intents = []
    for it in payload.get('intents', []):
        intent_name = it.get('intent')
        for t in it.get('text', []):
            texts.append(t)
            intents.append(intent_name)
    return texts, intents


def convert_to_spacy_format(texts, intents):
    labels = sorted(set(intents))
    examples = []
    for text, intent in zip(texts, intents):
        cats = {label: 1.0 if label == intent else 0.0 for label in labels}
        examples.append((text, {'cats': cats}))
    return examples, labels


def train(output_dir=MODEL_DIR, n_iter=10):
    texts, intents = load_intent_data()
    examples, labels = convert_to_spacy_format(texts, intents)

    nlp = spacy.blank('en')
    if 'textcat' in nlp.pipe_names:
        textcat = nlp.get_pipe('textcat')
    else:
        textcat = nlp.add_pipe('textcat', last=True, config={
            'exclusive_classes': True,
            'architecture': 'simple_cnn'
        })
    for label in labels:
        textcat.add_label(label)

    optimizer = nlp.begin_training()

    # Convert examples into spaCy's training format
    train_data = [(text, ann) for text, ann in examples]
    random.shuffle(train_data)

    with nlp.select_pipes(enable=['textcat']):
        for i in range(n_iter):
            losses = {}
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.5))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, losses=losses)
            print(f"Iteration {i+1}/{n_iter} - Losses: {losses}")

    # Create dir and save model
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_dir)
    print(f"Saved trained model to {output_dir}")


if __name__ == '__main__':
    train()
