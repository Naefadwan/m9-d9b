"""SPARQL -> Cypher Translation Task.

Each function returns a Cypher **string** whose executed result is
equivalent to the corresponding W9A SPARQL query (see the W9A drill at
`drill-9a-sparql/starter/queries/drill.py`). Equivalence is asserted by
the autograder as set-of-tuples equality on the named result columns,
ignoring row order (except where ORDER BY is part of the contract).

Run against the books mini-graph in `data/books_kg.cypher`.
"""


def q1() -> str:
    """Q1 — Return all (book, title) pairs.

    SPARQL equivalent: SELECT ?book ?title for every :Book with a :title.
    Cypher must return two columns named `book` and `title`. `book` is the
    Book entity's `id` (e.g., 'book:1'). Result set: 5 rows.
    """
    return "MATCH (b:Book) RETURN b.id AS book, b.title AS title"


def q2() -> str:
    """Q2 — Return (book, year) pairs filtered to books published after 2010.

    SPARQL equivalent: SELECT ?book ?year WHERE { ... FILTER (?year > 2010) }.
    Strict greater-than. Cypher must return columns named `book` (id string)
    and `year` (int). On the fixture: 1 row.
    """
    return "MATCH (b:Book) WHERE b.year > 2010 RETURN b.id AS book, b.year AS year"


def q3() -> str:
    """Q3 — Return all (book, author_name) pairs.

    SPARQL equivalent: one row per (book, author) edge; books with multiple
    authors produce multiple rows. Cypher must return columns named `book`
    (id string) and `author_name` (the Author's `name` property).
    On the fixture: 7 rows.
    """
    return "MATCH (b:Book)-[:AUTHORED_BY]->(a:Author) RETURN b.id AS book, a.name AS author_name"


def q4() -> str:
    """Q4 — Return (book, topic) pairs with topic OPTIONAL.

    SPARQL equivalent: every :Book appears in the result; ?topic is unbound
    for books with no :topic triple. In Cypher, an unmatched OPTIONAL value
    is NULL. Columns: `book` (id string), `topic` (string or NULL).
    On the fixture: 5 rows; one row has `topic` = NULL (book:2).
    """
    # Using the .topic property as it is NULL if missing on the node.
    return "MATCH (b:Book) RETURN b.id AS book, b.topic AS topic"


def q5() -> str:
    """Q5 — Return TRUE iff any book has more than one author.

    SPARQL equivalent: ASK with FILTER(?a1 != ?a2) over two distinct author
    bindings on the same book. Cypher must return a single column named
    `result` containing a single boolean row. Use a pattern that detects
    "exists a book with >=2 distinct authors" without enumerating them.

    On the fixture, book:1 (Hunt + Thomas) and book:5 (Fowler + Martin)
    both have multiple authors, so the expected value is TRUE.
    """
    return """
    RETURN EXISTS {
      MATCH (b:Book)-[:AUTHORED_BY]->(a1:Author), (b)-[:AUTHORED_BY]->(a2:Author)
      WHERE a1 <> a2
    } AS result
    """
