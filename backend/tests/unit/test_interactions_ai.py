"""Additional AI-generated unit tests for interaction filtering."""

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


# KEPT: verifies boundary behaviour when max_item_id == 0
def test_filter_with_zero_max_item_id() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 1, 1)]
    result = filter_by_max_item_id(interactions, max_item_id=0)
    assert len(result) == 1
    assert result[0].item_id == 0


# KEPT: covers edge case where the threshold is negative
def test_filter_with_negative_max_item_id_returns_empty() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 1, 1)]
    result = filter_by_max_item_id(interactions, max_item_id=-1)
    assert result == []


# KEPT: ensures filtering logic works correctly when item_id values are negative
def test_filter_handles_negative_item_ids() -> None:
    interactions = [_make_log(1, 1, -2), _make_log(2, 1, 1)]
    result = filter_by_max_item_id(interactions, max_item_id=0)
    assert len(result) == 1
    assert result[0].item_id == -2


# KEPT: verifies behaviour when every interaction is above the threshold
def test_filter_returns_empty_when_all_above_limit() -> None:
    interactions = [_make_log(1, 1, 5), _make_log(2, 1, 6)]
    result = filter_by_max_item_id(interactions, max_item_id=4)
    assert result == []


# DISCARDED: duplicates common equality-boundary coverage already present in the original tests
# def test_filter_returns_all_when_all_equal_to_limit() -> None:
#     interactions = [_make_log(1, 1, 3), _make_log(2, 2, 3)]
#     result = filter_by_max_item_id(interactions, max_item_id=3)
#     assert len(result) == 2


# KEPT: verifies that filtering preserves input order (important property of list comprehension)
def test_filter_preserves_original_order() -> None:
    interactions = [
        _make_log(1, 1, 5),
        _make_log(2, 1, 1),
        _make_log(3, 1, 3),
    ]
    result = filter_by_max_item_id(interactions, max_item_id=3)
    assert [i.id for i in result] == [2, 3]


# KEPT: ensures duplicates are handled correctly and not collapsed or skipped
def test_filter_handles_duplicate_item_ids() -> None:
    interactions = [
        _make_log(1, 1, 2),
        _make_log(2, 2, 2),
        _make_log(3, 3, 5),
    ]
    result = filter_by_max_item_id(interactions, max_item_id=2)
    assert len(result) == 2
    assert all(i.item_id == 2 for i in result)


# FIXED: strengthened assertion to verify identity preservation rather than relying only on equality
def test_filter_with_large_max_item_id_returns_all() -> None:
    interactions = [_make_log(1, 1, 10), _make_log(2, 1, 20)]
    result = filter_by_max_item_id(interactions, max_item_id=10_000)
    assert len(result) == 2
    assert result[0] is interactions[0]
    assert result[1] is interactions[1]


# KEPT: verifies exclusion behaviour for a single-element list
def test_filter_single_element_excluded() -> None:
    interactions = [_make_log(1, 1, 5)]
    result = filter_by_max_item_id(interactions, max_item_id=4)
    assert result == []


# DISCARDED: equality boundary case likely already covered in the original test suite
# def test_filter_single_element_included() -> None:
#     interactions = [_make_log(1, 1, 5)]
#     result = filter_by_max_item_id(interactions, max_item_id=5)
#     assert len(result) == 1
#     assert result[0].id == 1