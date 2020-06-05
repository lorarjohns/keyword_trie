import pytest
import re
from keyword_trie import Trie, Node

trie = Trie()

node = Node(data="")
sent = "The operations of each Borrower, and the activities of the officers and directors and, to the knowledge of each Borrower, any Subsidiaries of the Borrowers, employees, agents and representatives of each Borrower, while acting on behalf of such Borrower, and to the knowledge of each Borrower the operations of each Material Project Party in relation to the Project, have been conducted at all times in compliance with all applicable Anti-Money Laundering Laws, Sanctions, and Anti-Corruption Laws.".lower().split()
keywords = [["Project"],
            "Project Manager".split(),
            "Anti-Money Laundering Laws".split(),
            "Material Project Party".split(),
            "Anti-Corruption Laws".split()]
phrase_tests = [
    (sent, keywords, ['material project party', 'project', 'anti-money laundering law', 'anti-corruption law'])
]

expected_keys = ['material project party', 'project', 'anti-money laundering law', 'anti-corruption law']

for key in keywords:
    trie.add(key)


def test_node():
    node.children = {"a": {"c": {}}, "b": {"d": {}}}
    assert node[["a"]] == [{"c": {}}]