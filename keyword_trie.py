"""
Program to extract keywords from document.

Usage:
  keyword_trie.py --keywords=<file> <textfiles>... [options]

Options:

  --debug=bool   Run logger in debug mode   [default: false]
  --print=bool   Print matches to the terminal   [default: true]
"""

import logging
from logging import Logger, log
from docopt import docopt
from typing import List, Dict
from textutil import TextUtil

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Node:
    def __init__(self, data: str = None):
        self.data = data
        self.children: Dict = dict()
        self.EOS: bool = False

    def addChild(self, key):
        if not isinstance(key, Node):
            self.children[key] = Node(key)
        else:
            self.children[key.data] = key

    def __getitem__(self, data: List[str]):
        return [self.children[key] for key in data]

    def __repr__(self):
        return f"<Node {self.data} : children {self.children.keys()}>"

class Trie:
    def __init__(self):
        self.head = Node()

    def __getitem__(self, key):
        return self.head.children[key]

    def add_many(self, list_data):
        for item in list_data:
            self.add(item)

    #def add(self, data):
    #    current_node = self.head
    #    current_node.EOS = False
#
    #    for key in data:
    #        if key in current_node.children:
    #            current_node = current_node.children[key]
    #        else:
    #            current_node.addChild(key)
    #            current_node = current_node.children[key]
    #    else:
    #        current_node.EOS = True
#
    #    # store the full phrase at end node
    #    current_node.data = " ".join(data)

    def add(self, data):
        current_node = self.head

        for key in data:
            if key in current_node.children:
                current_node = current_node.children[key]
            else:
                current_node.addChild(key)
                current_node = current_node.children[key]
        else:
            # store the full phrase at end node
            current_node.EOS = True
            current_node.data = " ".join(data)

    def find_phrases(self, text):
        '''
        Finds phrases in text that are in the trie.
        @param text: text to search

        '''
        found = []
        current_node = self.head
        
        for key in text:
            #logger.debug(f"key:::{key}")
            #logger.debug(f"current:::{current_node}")
            if key in current_node.children:
                current_node = current_node.children[key]
                if current_node.EOS:
                    found.append(current_node.data)
                    #logger.debug(f"appending {current_node.data}")
                    if len(current_node.children) == 0:
                        current_node = self.head
                    continue
            else:
                #logger.debug(f"ELSE {key}")
                if current_node.EOS:
                    found.append(current_node.data)
                    #logger.debug(f"appending {current_node.data}")
                current_node = self.head
        else:
            if current_node.EOS:
                found.append(current_node.data)
                #logger.debug(f"appending {current_node.data}")
                current_node = self.head
        return found

    def has_word(self, data):
        """
        Return True or False based on whether the word is in the trie.
        @param data: the word to search
        @returns boolean
        """
        if len(data) == 0:
            return False
        if data is None:
            raise ValueError("Input can't be null.")

        # Start at the top
        current_node = self.head
        exists = True

        for key in data:
            if key in current_node.children:
                current_node = current_node.children[key]
            else:
                exists = False
                break

        # Check if in vocabulary
        if exists:
            if current_node.data is None:
                exists = False

        return exists

    def start_with_prefix(self, prefix: List[str]) -> List[str]:
        """
        Return a list of all words in trie that start with prefix.
        @param prefix: the prefix to search. (Breadth first)
        """
        words = list()
        if prefix is None:
            raise ValueError("Prefix cannot be null")

        # Determine end-of-prefix node
        top_node = self.head
        for key in prefix:
            if key in top_node.children:
                top_node = top_node.children[key]
            else:
                # Prefix not in tree, stop
                return words

        # Get words under prefix
        if top_node == self.head:
            queue = [node for key, node in top_node.children.items()]
        else:
            queue = [top_node]

        # do a breadth first search under the prefix
        # A side effect of using BFS is that we get
        # a list of phrases by increasing length
        while queue:
            current_node = queue.pop()
            if current_node.data is not None:
                words.append(current_node.data)

            queue = [node for key, node in current_node.children.items()] + queue

        return words

    def getData(self, data):
        """ This returns the key of the node identified by the given word """

        current_node = self.head
        for key in data:
            current_node = current_node.children[key]

        return current_node.data


def load_text(text_file):
    """
    load text from file
    @param text_file: target text
    @returns string of text
    """
    with open(text_file, "r") as f:
        return f.read()


def main():
    """
    Main function:
        - Gets keywords from file and processes them
        - Constructs a trie with the words as nodes
        - Consumes a text or list of texts from the user
        - Performs a linear search to determine whether a text
          contains the terms of interest and reports which relevant
          terms appear in which documents
    """
    args = docopt(__doc__)



    if args["--debug"] == "true":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)

    logger.debug(f"Keyword file: {args['--keywords']}")
    util = TextUtil(vocab_file=args["--keywords"])

    keywords = util.vocab_lemmata

    num_docs = len(args["<textfiles>"])

    trie = Trie()
    trie.add_many(keywords)
    #logger.debug([[node for key, node in subnode.children.items()] for subnode in trie.head.children.values()])
    #logger.debug(trie.head.children.keys())
    for i, doc in enumerate(args["<textfiles>"]):
        print(f"Searching doc {i+1} of {num_docs}...")

        text = util.preprocess(load_text(doc))
        hits = trie.find_phrases(text)
        kwset = set([" ".join(k) for k in keywords])
        logger.debug(f" hits :{set(hits)}, kw: {kwset}")
        if hits is not None:
            print(f"{len(hits)} matches found!")
            print("\nMatching keywords:\n")
            print("-" * 40)
            if args["--print"] == "true":
                for match in set(hits):
                    if match:
                        print(match)
                print("-" * 40)
            with open("trie_output.txt", "a") as f:
                f.write(args["<textfiles>"][i] + "\t")
                for match in hits:
                    try:
                        f.write(match + "\t")
                    except TypeError as e:
                        logger.debug(f"Match cannot be written: {e}")
                        continue
                f.write("\n")


if __name__ == "__main__":
    main()
