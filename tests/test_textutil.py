import pytest
import re
from textutil import TextUtil

text = "The operations of each Borrower, and the activities of the officers and \
    directors and, to the knowledge of each Borrower, any Subsidiaries of the Borrowers, \
    employees, agents and representatives of each Borrower, while acting on behalf \
    of such Borrower, and to the knowledge of each Borrower the operations  \
    of each Material Project Party in relation to the Project, have been conducted at all times \
    in compliance with all applicable Anti-Money Laundering Laws, Sanctions, and Anti-Corruption Laws. \
    Neither Borrower, nor any Subsidiaries of the Borrowers, nor any officer or director or, \
    to the knowledge of any Borrower, Affiliates, employee, agent or representative of \
    either Borrower has engaged, directly or indirectly, in any activity \
    or conduct which would violate any Anti-Corruption Laws or Anti-Money Laundering Laws. \
    Neither Borrower nor any Subsidiaries of the Borrowers, nor any officer or director \
    or, to the knowledge of any Borrower, Affiliates, employee, agent or representative of either Borrower \
    has engaged, directly or indirectly, in any dealings or transactions with, \
    involving or for the benefit of a Sanctioned Person, or in or involving a Sanctioned Country, \
    where such dealings or transactions would violate Sanctions,\
    in the five (5) year period immediately preceding the date hereof."

vocab = [
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
        "Agents",
    ]

preprocessor = TextUtil("vocab")

keywords = [
        ("Person", "involving or for the benefit of a Sanctioned Person, or in or involving a Sanctioned Country"),
        #("Officer", "nor any officer or director or, to the knowledge of any Borrower, Affiliates, employee, agent or representative of either Borrower"),
        #("Director", "and the activities of the officers and directors and, to the knowledge of each Borrower, any Subsidiaries of the Borrowers"),
        ("Agents", "the knowledge of any Borrower, Affiliates, employee, agent or representative of \
                either Borrower has engaged, directly or indirectly, in any activity or conduct which \
                    would violate any Anti-Corruption Laws or Anti-Money Laundering Laws"),
        ("Borrower", "The operations of each Borrower, and the activities of the officers and \
    directors and, to the knowledge of each Borrower, any Subsidiaries of the Borrowers,")

]



lemmatized_vocab = [

(['borrower']),
(['subsidiary']),
(['material', 'project', 'party']),
(['project']),
(['project', 'manager']),
(['anti-money', 'laundering', 'law']),
(['sanction']),
(['anti-corruption', 'law']),
(['affiliate']),
(['sanction', 'person']),
(['sanction', 'country']),
(['person']),
(['officer']),
(['director']),
(['agent'])

]
#def test_pipeline():
#    output = preprocessor.preprocess(text)

@pytest.mark.parametrize("actual, expected", zip(preprocessor.vocab, vocab))
def test_load(actual, expected):
    assert actual == expected

@pytest.mark.parametrize("expected", lemmatized_vocab)
def test_lemmatizer(expected):
    assert expected in preprocessor.vocab_lemmata