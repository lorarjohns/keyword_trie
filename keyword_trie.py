'''
Program to extract keywords from document.

Usage:
  keyword_trie.py --keywords=<file> <textfiles>... [options]

Options:

  --debug=bool   Run logger in debug mode   [default: true]
  --print=bool   Print matches to the terminal   [default: true]
'''

import logging
from docopt import docopt
from typing import Text, List, Dict, Optional, Union
from textutil import TextUtil

class Node:
    def __init__(self, data: str=None):
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

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]

    def add_many(self, list_data):
        for item in list_data:
            self.add(item)
    
    def add(self, data):
        current_node = self.head
        current_node.EOS = False
        
        for key in data:
            if key in current_node.children:
                current_node = current_node.children[key]
            else:
                current_node.addChild(key)
                current_node = current_node.children[key]
        else:
            current_node.EOS = True
        
        # store the full phrase at end node
        current_node.data = " ".join(data)
    
    def find_phrases(self, text):
        found = []
        current_node = self.head
        for key in text:
            if key in current_node.children:
                current_node = current_node.children[key]
            else:
                if current_node.data is not None:
                    found.append(current_node.data)
                current_node = self.head
        found.append(current_node.data)
        return found 
    
    def has_word(self, data):
        '''
        Return True or False based on whether the word is in the trie.
        @param data: the word to search
        @returns boolean
        '''
        if len(data) == 0:
            return False
        if data == None:
            raise ValueError('Input can\'t be null.')
        
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
            if current_node.data == None:
                exists = False
        
        return exists
    
    def start_with_prefix(self, prefix: List[str]) -> List[str]:
        """
        Return a list of all words in trie that start with prefix.
        @param prefix: the prefix to search. (Breadth first)
        """
        words = list()
        if prefix == None:
            raise ValueError('Prefix cannot be null')
        
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
            if current_node.data != None:
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
    '''
    load text from file
    @param text_file: target text
    @returns string of text
    '''
    with open(text_file, 'r') as f:
        return f.read()

def main():
    
    args = docopt(__doc__)
        
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    if args["--debug"] == 'true':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)


    logger.debug(args)
    logger.debug(f"Keyword file: {args['--keywords']}")
    util = TextUtil(vocab_file=args["--keywords"])
    
    keywords = util.vocab_lemmata

    num_docs = len(args["<textfiles>"])

    trie = Trie()
    trie.add_many(keywords)
    logger.debug(f"Root children: {trie.head.children.keys()}")

    for i, doc in enumerate(args["<textfiles>"]):
        print(f"Searching doc {i+1} of {num_docs}...")
        
        text = util.preprocess(load_text(doc))
        hits = trie.find_phrases(text)

        if hits is not None:
            print(f"{len(hits)} matches found!")
            print("-"*40)
            if args["--print"] == 'true':
                for match in hits:
                    if match:
                        print(match)
                print("-"*40)
            with open("trie_output.txt", "a") as f:
                f.write(args["<textfiles>"][i])
                for match in hits:
                    try:
                        f.write("\t" + match)
                    except TypeError as e:
                        logger.debug(f"Match cannot be written: {e}")
                        continue

if __name__ == '__main__':
    main()
    #main()
    #trie = Trie()
    #sent = "The operations of each Borrower, and the activities of the officers and directors and, to the knowledge of each Borrower, any Subsidiaries of the Borrowers, employees, agents and representatives of each Borrower, while acting on behalf of such Borrower, and to the knowledge of each Borrower the operations of each Material Project Party in relation to the Project, have been conducted at all times in compliance with all applicable Anti-Money Laundering Laws, Sanctions, and Anti-Corruption Laws."
    #keywords = ["Project",
    #        "Project Manager",
    #        "Anti-Money Laundering Laws",
    #        "Material Project Party",
    #        "Anti-Corruption Laws"]
    #
    #u = TextUtil(keywords)
    #proc = u.preprocess(sent.lower())
#
    #kw = [u.preprocess(k.lower()) for k in keywords]
#
    #trie = Trie()
    ##for k in kw:
    #    #trie.add(k)
    #trie.add_many(kw)
#
#
    #print(trie.find_phrases(proc))