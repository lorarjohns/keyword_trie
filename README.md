<h1 align="center">Keyword Trie</h1>

> Trie search with keyword nodes

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

- I had an index-returning function for where in the text
  the matches occur, but benchmarks were weirdly slow,
  so that needs to be revisited
- The processing and search could be better integrated and
  sped up -- utilizing something like spaCy's PhraseMatcher,
  which is a trie-based implementation of a search, could
  leverage the speed enhancements of the c structs to actually
  do something like this in production.
- If not returning indexes or fulltext/span context matches,
  then deduplicate matches. They are deduped in the printing
  (Update - I realized in my haste I did something dumb in the
  find_phrases algo -- fixing now, the `None`s are gone but I
  am aware of the breadth search problem that I introduced by typo'ing!
  Commit will come when I get another break.)
- Fix prefix collapsing for some phrases

## Author

👤 **Ray (Lora) Johns**

* Website: www.espritdecorpus.com
* Github: [@lorarjohns](https://github.com/lorarjohns)
* LinkedIn: [@lora-johns](https://linkedin.com/in/lora-johns)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_