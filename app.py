import random
import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def reset_game(low: int, high: int): #FIX: created a reset funtion to handle new game bug, eith agent mode
    """Set all game state back to a fresh starting round."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []


if "secret" not in st.session_state:
    reset_game(low, high)

st.subheader("Make a guess")

attempts_banner = st.empty()  # FIX: reserve banner slot; filled after attempts updates (display-lag fix)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

with st.form(key=f"guess_form_{difficulty}", clear_on_submit=True):#FIX: text input and submit button wrapped in st.form to alloe Enter to trigger submit, using agent mode
    raw_guess = st.text_input("Enter your guess:")
    submit = st.form_submit_button("Submit Guess 🚀")

col2, col3 = st.columns(2)
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    reset_game(low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    attempts_banner.info(  # FIX: keep banner visible on win/loss screen before st.stop()
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
    )
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret) #FIX: Refactored logic into logic_utils.py using agent mode).

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )

    # FIX: check loss for ANY submitted attempt (valid or invalid), not just valid guesses, using AI agent
    if st.session_state.status == "playing" and st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"
        st.error(
            f"Out of attempts! "
            f"The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        )

attempts_banner.info(  # FIX: fill banner AFTER attempts is incremented (display-lag fix)
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
