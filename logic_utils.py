def get_range_for_difficulty(difficulty: str):#FIX: Refactored logic into logic_utils.py using agent mode
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):#FIX: Refactored logic into logic_utils.py using agent mode
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret): #FIX: Refactored logic into logic_utils.py using agent mode
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):#FIX: Refactored logic into logic_utils.py using agent mode
    
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX, allows first guess to get a 100
        points = 100 - 10 * (attempt_number - 1) 
        if points < 10:
            points = 10
        return current_score + points

    # Any wrong guess (Too High or Too Low) costs the same flat penalty.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
