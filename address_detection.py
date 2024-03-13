from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("konverner/distilcamembert-base-ner-address")
model = AutoModelForTokenClassification.from_pretrained("konverner/distilcamembert-base-ner-address")

ner = pipeline(
    task='ner',
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

def extract_address_using_bert(text):
    if text is None or "":
        return None , None
    else:
        result = ner(text)
        address , score = [r['word'] for r in result] , [r['score'] for r in result]
    return address , score 

def process_subtexts(subtexts):
    addresses = []
    scores = []

    for subtext in subtexts:
        if subtext:  # Check if subtext is not empty
            address, score = extract_address_using_bert(subtext)
            addresses.extend(address)
            scores.extend(score)

    return addresses, scores