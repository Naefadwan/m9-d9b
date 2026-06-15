"""Learner-written tests for queries/warmups.py.

You write at least 2 tests here. The autograder verifies each test
function contains at least one assertion and is not left as the
placeholder `pytest.fail("Not implemented")`.

A driver fixture (`driver`) is provided via conftest.py — it points at
the same Neo4j instance the autograder uses, with the drill fixtures
already loaded. Run a Cypher string in a session like:

    with driver.session() as session:
        rows = list(session.run(cypher_str, params))

Test ideas:
  - Confirm `q1_list_recipes()` returns exactly the 5 recipe names you
    expect from `recipes_mini.cypher`.
  - Confirm `q2_filter_by_cuisine("Italian")` returns the two Italian
    recipes only — no Chinese or Sichuan recipes.
  - Confirm `q3_subclass_traversal("Chinese")` includes Sichuan recipes
    (via :SUBCLASS_OF) but `q2_filter_by_cuisine("Chinese")` does not.
"""

import pytest

from queries.warmups import q1_list_recipes, q2_filter_by_cuisine, q3_subclass_traversal


def test_q1_list_recipes_returns_all_five(driver):
    """Confirm q1_list_recipes() returns exactly the 5 recipe names."""
    query = q1_list_recipes()
    with driver.session() as session:
        result = list(session.run(query))

    names = {record["name"] for record in result}
    expected_names = {
        "Margherita Pizza",
        "Pesto Pasta",
        "Mapo Tofu",
        "Kung Pao Chicken",
        "Ginger Scallion Noodles",
    }
    assert names == expected_names
    assert len(result) == 5


def test_q3_traversal_picks_up_subclasses(driver):
    """Confirm q3_subclass_traversal("Chinese") includes Sichuan recipes."""
    # q2 for Chinese should only return 'Ginger Scallion Noodles'
    query_q2, params_q2 = q2_filter_by_cuisine("Chinese")
    with driver.session() as session:
        result_q2 = list(session.run(query_q2, params_q2))

    names_q2 = {record["name"] for record in result_q2}
    assert names_q2 == {"Ginger Scallion Noodles"}

    # q3 for Chinese should return 'Ginger Scallion Noodles' AND 'Mapo Tofu' AND 'Kung Pao Chicken'
    query_q3, params_q3 = q3_subclass_traversal("Chinese")
    with driver.session() as session:
        result_q3 = list(session.run(query_q3, params_q3))

    names_q3 = {record["name"] for record in result_q3}
    assert names_q3 == {"Ginger Scallion Noodles", "Mapo Tofu", "Kung Pao Chicken"}
