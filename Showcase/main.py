
import re
import spacy as sp
from spacy.language import Language
from spacy.tokens import Span, Doc
with open("Showcase/sample.txt", "r") as f:
    source = f.read()
english = sp.load("en_core_web_sm")
@Language.component("addresses")
def searchNames(doc: Doc) -> Doc:
    """Searches for names in the text marked with addressing and adds them to the named entities."""
    #The pattern expression searches for names with addresses Mr., Mrs., Ms., Dr., Prof., etc.
    pattern = re.compile(r"(P|M|D)(r|s)(s|.)?") #(f|.)?\s[A-Z][a-z]+
    matches = [(match.start, match.end) for match in pattern.finditer(doc.text)]
    #Add the names to the named entities.
    names = [Span(doc, start, end, "PERSON") for start, end in matches]
    doc.ents = tuple(list(doc.ents) + names)
    return doc
    #for match in pattern.finditer(doc.text):
    #    print(doc.text[match.start():match.end()])
    #    print(match)
#english.remove_pipe("filter")
english.add_pipe("addresses")
chocolate = english(source)
for entity in chocolate.ents:
    if entity.label_ == "PERSON":
        print(entity.text, entity.label_)
