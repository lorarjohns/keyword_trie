# Keyword Trie

## Trie search with keyword nodes

## Setup

Create a virtual environment and install necessary packages:

```sh
pip install -r requirements.txt
```

## Usage

```sh
python keyword_trie.py --keywords=<file> <textfile>...
```

## Run tests

```sh
py.test --doctest-modules
```

## To Do

- Lemma-to-original lookup to return the input text's surface form.
- See what happens if tokenizing 'anti-' prefix separately, so all 'anti-'
  words are under the same subtree.
- Return text indices for matches
- Integrate and optimize text processing and search: utilizing something like spaCy's PhraseMatcher,
  which is a trie-based implementation, could
  leverage the speed enhancements of the underlying c structs to actually
  do something like this in production.

## Changes

### 2020-06-06

- Fixed prefix collapsing for some phrases: the way I originally wrote this,
  it was a problem for single-word vs. multi-word phrases where the single-
  word keyword is a substring of the longer keyword. An annoying consequence
  of using words as keys instead of characters, and my initial choice of
  storing the whole keyword as the node's key, is that I overwrote single-word
  keys when they're part of a longer key.
  (Example: node 'project' gets overwritten when keyword 'project manager' is added.)
  Fixed by changing the `add` and `find_phrases` logic. Better would be to refactor
  the way the objects are stored.

## Author

👤 **Ray (Lora) Johns**

* Website: www.espritdecorpus.com
* Github: [@lorarjohns](https://github.com/lorarjohns)
* LinkedIn: [@lora-johns](https://linkedin.com/in/lora-johns)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_