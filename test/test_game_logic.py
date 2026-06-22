import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_correct_guess_wins():
    outcome, message = check_guess(42, 42)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high_says_go_lower():
    # Guess is greater than the secret -> player should aim LOWER.
    outcome, message = check_guess(80, 30)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_guess_too_low_says_go_higher():
    # Guess is less than the secret -> player should aim HIGHER.
    outcome, message = check_guess(10, 30)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


@pytest.mark.parametrize(
    "guess, secret, expected_outcome",
    [
        (2, 1, "Too High"),
        (1, 2, "Too Low"),
        (100, 99, "Too High"),
        (99, 100, "Too Low"),
        (50, 50, "Win"),
    ],
)
def test_outcome_matches_numeric_comparison(guess, secret, expected_outcome):
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected_outcome


def test_hint_direction_is_not_swapped():
    # Regression guard: the message must point the OPPOSITE way of the error.
    _, high_message = check_guess(90, 50)   # guessed too high
    _, low_message = check_guess(10, 50)    # guessed too low
    assert "LOWER" in high_message
    assert "HIGHER" in low_message


@pytest.mark.parametrize(
    "difficulty, expected_range",
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 50)),
    ],
)
def test_known_difficulties_return_expected_range(difficulty, expected_range):
    assert get_range_for_difficulty(difficulty) == expected_range


def test_unknown_difficulty_falls_back_to_default_range():
    # Anything outside the known set should default to the Normal range.
    assert get_range_for_difficulty("Impossible") == (1, 100)


def test_parse_guess_accepts_plain_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_truncates_decimal_input():
    # A decimal string is accepted and truncated toward zero.
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_guess_rejects_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_rejects_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_rejects_non_numeric_input():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_first_guess_win_awards_ninety():
    # attempt_number is 1-based, so winning on the first guess gives 90.
    assert update_score(0, "Win", 1) == 90


@pytest.mark.parametrize(
    "attempt_number, expected_points",
    [
        (1, 90),
        (2, 80),
        (5, 50),
        (9, 10),
    ],
)
def test_win_points_decrease_with_more_attempts(attempt_number, expected_points):
    # Each extra attempt costs 10 points off a fresh score.
    assert update_score(0, "Win", attempt_number) == expected_points


def test_win_points_are_floored_at_ten():
    # A very late win should never award less than 10 points.
    assert update_score(0, "Win", 20) == 10


def test_win_adds_to_existing_score():
    # Points are added on top of the current score, not replacing it.
    assert update_score(45, "Win", 1) == 135


@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4])
def test_too_high_always_costs_five(attempt_number):
    # Regression guard: a wrong guess must never depend on attempt parity.
    assert update_score(50, "Too High", attempt_number) == 45


@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4])
def test_too_low_always_costs_five(attempt_number):
    assert update_score(50, "Too Low", attempt_number) == 45


def test_wrong_guesses_are_penalized_equally():
    # Too High and Too Low are equivalent outcomes and must score the same.
    assert update_score(50, "Too High", 2) == update_score(50, "Too Low", 2)


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(50, "Unknown", 1) == 50
