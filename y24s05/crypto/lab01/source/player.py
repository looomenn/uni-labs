from letterguesser.logic.AutoPlayer import AutoPlayer
from solve import load_analysis, LANGUAGE

FREQUENCIES: dict = {}


def static_guess(data: dict) -> tuple[str, str]:
    """
    Guess the next letter based on the letter frequency.

    :param data: Experiment data passed from AutoPlayer.
    """
    global FREQUENCIES

    visible_text = data['text']
    if not visible_text:
        raise ValueError("No visible text to analyze.")

    last_char = visible_text[-1]
    last_char = last_char.replace(' ', '_')

    possible_bigrams = {
        bigram: freq
        for bigram, freq in FREQUENCIES.items()
        if bigram.startswith(last_char)
    }

    valid_bigrams = {
        bigram: freq
        for bigram, freq in possible_bigrams.items()
        if bigram[1].replace(" ", "_") not in data["used_letters"]
    }

    if not valid_bigrams:
        print("[DEBUG] No valid bigrams for current character. Fallback triggered.")
        valid_bigrams = {
            bigram: freq
            for bigram, freq in FREQUENCIES.items()
            if bigram[1].replace(" ", "_") not in data["used_letters"]
        }

    if not valid_bigrams:
        raise ValueError("No remaining letters to guess.")

    best_bigram = max(valid_bigrams, key=valid_bigrams.get)
    guess = best_bigram[1]
    return guess, 'custom'


def main():
    """Entry point."""
    analysis = load_analysis(f'./analysis_{LANGUAGE}.json')

    global FREQUENCIES
    FREQUENCIES = analysis['normalized_bigram_frequencies']

    player = AutoPlayer(
        alphabet=LANGUAGE,
        save_folder='./runs',
        guess_function=static_guess
    )

    print("[INFO] Starting the AutoPlayer game...")
    player.play_game(num_games=50, ngram_order=30)


if __name__ == "__main__":
    main()
