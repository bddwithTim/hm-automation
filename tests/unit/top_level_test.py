from src.utils.utils import MergeStrategy, deep_merge_dict


def test__deep_merge_dict__empty_base():
    base = {}
    addition = {"A": 1}
    assert deep_merge_dict(base, addition) == {"A": 1}


def test__deep_merge_dict__empty_addition():
    base = {"A": 1}
    addition = {}
    assert deep_merge_dict(base, addition) == {"A": 1}


def test__deep_merge_dict__no_shared_keys():
    base = {"A": 1, "B": 2}
    addition = {"C": 3}
    assert deep_merge_dict(base, addition) == {"A": 1, "B": 2, "C": 3}


def test__deep_merge_dict__some_shared_keys():
    base = {"A": 1, "B": 2}
    addition = {"B": 5, "C": 3}
    assert deep_merge_dict(base, addition) == {"A": 1, "B": 5, "C": 3}


def test__deep_merge_dict__identical():
    base = {"A": 1, "B": 2}
    addition = {"A": 1, "B": 2}
    assert deep_merge_dict(base, addition) == {"A": 1, "B": 2}


def test__deep_merge_dict__nested():
    base = {"A": 1, "B": {"C": 3}}
    addition = {"B": {"C": 4}}
    assert deep_merge_dict(base, addition) == {"A": 1, "B": {"C": 4}}


def test__deep_merge_dict__with_strategy_to_delete_key_when_present():
    base = {"A": {"B": 1, "C": 2}}
    addition = {"A": {"B": MergeStrategy.DeleteKey}}
    assert deep_merge_dict(base, addition) == {"A": {"C": 2}}


def test__deep_merge_dict__with_strategy_to_delete_key_when_absent():
    base = {"A": 1}
    addition = {"Z": MergeStrategy.DeleteKey}
    assert deep_merge_dict(base, addition) == {"A": 1}
