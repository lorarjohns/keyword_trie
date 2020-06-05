from logging import disable
import re
import string
import logging
import json

from typing import List, Callable, Pattern

import spacy
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex

punct = list(string.punctuation)
punct.remove("-")
punct = "".join(punct)

RE_PUNCT = re.compile(fr"([{re.escape(punct)}])+", re.UNICODE)
RE_NUMERIC = re.compile(r"[0-9]+", re.UNICODE)
RE_SENT = re.compile(r"(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)", re.UNICODE)
RE_ENT = re.compile(r"((?<!^)(?<!\.\s)([A-Z][a-z|-]+\s?)+)", re.UNICODE)
RE_SPACE = re.compile(r"(\s)+", re.UNICODE)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.DEBUG)


class TextUtil(dict):
    """
    Utility class to use trie.
    """

    def __init__(self, vocab_file=None, vocab=None):
        self.vocab = vocab or self.load_vocab(vocab_file)
        self.docs = []
        self.nlp = NLP().nlp
        self.vocab_lemmata = [
            [t.lemma_ for t in keyword]
            for keyword in self.nlp.pipe(map(str.lower, self.vocab))
        ]
        self.dict = {
            " ".join(lem): kw for lem, kw in zip(self.vocab_lemmata, self.vocab)
        }
        self.pipeline = [  # QUESTIONS: split on hyphens? (e.g. 'anti-' compounds); stopwords/min length?
            lambda x: x.lower(),
            self._strip,
            self._lemmatize,
        ]

    def load_vocab(self, vocab_file):
        """
        load vocab from file
        @param vocab_file: file path
        @returns list of keywords
        """
        with open(vocab_file, "r") as f:
            return [w.strip() for w in f.readlines()]

    def preprocess(self, text: str, funcs: List[Callable[..., str]] = None) -> str:
        """
        @param text: the text to process
        @param funcs: a list of preprocessing steps to apply [default: self.pipeline]
        @returns the text in processed form

        # TODO: Make a spacy pipeline.
        """

        funcs = self.pipeline

        result = text
        for fn in funcs:
            try:
                result = fn(result)
            except Exception as e:
                logger.debug(f"Function: {fn.__str__()}")
                logger.debug(f"Error: {e}")
                logger.debug(f"Type of input was: {type(result)}")

        self.docs.append(result)
        return result

    """
    Text normalization utils.
    """

    def _strip(
        self, text: str, patterns: List[re.Pattern] = [RE_PUNCT, RE_NUMERIC, RE_SPACE]
    ) -> str:
        """
        @param text: string
        @param patterns: list of regex patterns for substitution
        @returns sentences with elements removed.

        Example:

        _strip("Th15 s3nt3nce has   space,,, numb3r5 and punctuation!!", [RE_PUNCT, RE_NUMERIC, RE_SPACE])
        Th s nt nce has space numb r and punctuation 
        """
        for pattern in patterns:
            text = pattern.sub(r" ", text)
        return text

    def _lemmatize(self, text: str) -> List[str]:
        return [token.lemma_ for token in self.nlp(text, disable=["ner"])]


class NLP:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        infixes = (
            LIST_ELLIPSES
            + LIST_ICONS
            + [
                r"(?<=[0-9])[+\-\*^](?=[0-9-])",
                r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                    al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                ),
                r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                # EDIT: commented out regex that splits on hyphens between letters:
                # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
                r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
            ]
        )
        infix_re = compile_infix_regex(infixes)
        self.nlp.tokenizer.infix_finditer = infix_re.finditer


if __name__ == "__main__":
    pass
