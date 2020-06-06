from textutil import TextUtil
import pytest
import re
from keyword_trie import Trie, Node

trie = Trie()

node = Node(data="")
text = "The operations of each Borrower, and the activities of the officers and directors and, to the knowledge of each Borrower, any Subsidiaries of the Borrowers, employees, agents and representatives of each Borrower, while acting on behalf of such Borrower, and to the knowledge of each Borrower the operations of each Material Project Party in relation to the Project or Project Manager, have been conducted at all times in compliance with all applicable Anti-Money Laundering Laws, Sanctions, and Anti-Corruption Laws. Neither Borrower, nor any Subsidiaries of the Borrowers, nor any officer or director or, to the knowledge of any Borrower, Affiliates, employee, agent or representative of either Borrower has engaged, directly or indirectly, in any activity or conduct which would violate any Anti-Corruption Laws or Anti-Money Laundering Laws. Neither Borrower nor any Subsidiaries of the Borrowers, nor any officer or director or, to the knowledge of any Borrower, Affiliates, employee, agent or representative of either Borrower has engaged, directly or indirectly, in any dealings or transactions with, involving or for the benefit of a Person or Sanctioned Person, or in or involving a Sanctioned Country, where such dealings or transactions would violate Sanctions, in the five (5) year period immediately preceding the date hereof."
sent = "The operations of each Borrower, and the activities of the officers and directors and, to the knowledge of each Borrower, any Subsidiaries of the Borrowers, employees, agents and representatives of each Borrower, while acting on behalf of such Borrower, and to the knowledge of each Borrower the operations of each Material Project Party in relation to the Project, have been conducted at all times in compliance with all applicable Anti-Money Laundering Laws, Sanctions, and Anti-Corruption Laws.".lower().split()
keywords = [
    ["Project"],
    "Project Manager".split(),
    "Anti-Money Laundering Laws".split(),
    "Material Project Party".split(),
    "Anti-Corruption Laws".split(),
]
phrase_tests = [
    (
        sent,
        keywords,
        [
            "material project party",
            "project",
            "anti-money laundering law",
            "anti-corruption law",
        ],
    )
]

expected_keys = [
    "material project party",
    "project",
    "anti-money laundering law",
    "anti-corruption law",
]

for key in keywords:
    trie.add(key)


def test_node():
    node.children = {"a": {"c": {}}, "b": {"d": {}}}
    assert node[["a"]] == [{"c": {}}]

def test_trie():
    keywords = [
        "Borrower",
        "Subsidiaries",
        "Material Project Party",
        "Project",
        "Project Manager",
        "Anti-Money Laundering Laws",
        "Sanctions",
        "Anti-Corruption Laws",
        "Affiliates",
        "Sanctioned Person",
        "Sanctioned Country",
        "Person",
        "Officer",
        "Director",
        "Agents"
    ]
    trie = Trie()
    util = TextUtil(vocab=keywords)
    doc = util.preprocess(text)
    trie.add_many(util.vocab_lemmata)
    hits = set(trie.find_phrases(doc))
    kwset = set([" ".join(k) for k in util.vocab_lemmata])
    assert len(hits.difference(kwset)) == 0
    assert hits == kwset