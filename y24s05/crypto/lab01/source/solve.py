"""
This module contains the functions that solve the problem.
"""

import re
import math
import json
from datetime import datetime
from collections import Counter
from pathlib import Path

ALPHABET_EN: str = 'abcdefghijklmnopqrstuvwxyz '
ALPHABET_UK: str = 'йцукенгшщзхїфівапролджєґячсмитьбю '

LANGUAGE: str = 'uk'


def calc_freq(text: str) -> dict[str, float]:
    """Calculate the frequency of each letter in a text."""
    total_chars = len(text)
    frequencies = Counter(text)
    return {char: count / total_chars for char, count in frequencies.items()}


def calc_ngram_freq(text: str, n: int) -> dict[str, float]:
    """
    Calculate the frequencies of n-grams in the text.

    :param text: Input text.
    :param n: N-gram order.
    :return: A dictionary of n-gram frequencies.
    """
    ngrams = [text[i:i + n] for i in range(len(text) - n + 1)]
    total_ngrams = len(ngrams)
    counter = Counter(ngrams)
    return {ngram: count / total_ngrams for ngram, count in counter.items()}


def calc_bigram_freq(text: str, crossing: bool = True) -> dict[str, float]:
    """
    Calculate bigram frequencies with or without crossing spaces.

    :param text: Input text.
    :param crossing: Whether to include spaces as valid characters in bigrams.
    :return: Dictionary of bigram frequencies.
    """
    bigrams: list = []

    if crossing:
        bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    else:
        for word in text.split():
            bigrams.extend([word[i:i + 2] for i in range(len(word) - 1)])

    total_bigrams = len(bigrams)
    frequencies = Counter(bigrams)
    return {bigram: count / total_bigrams for bigram, count in frequencies.items()}


def calc_entropy(freq: dict[str, float]) -> float:
    """Calculate the entropy for a given frequency distribution."""
    return -sum(p * math.log2(p) for p in freq.values() if p > 0)


def calc_redundancy(
        entropy: float,
        alphabet_size: int,
        is_bigram: bool = False
) -> float:
    """Calculate redundancy based on entropy and alphabet size."""
    log = math.log2(alphabet_size)

    max_entropy = 2 * log if is_bigram else log
    return 1 - (entropy / max_entropy)


def load_text(file_path: str | Path) -> str:
    """
    Load text from a file, ensuring the file exists.

    :param file_path: Path to the text file.
    :return: The content of the file as a string.
    :raises FileNotFoundError: If the file does not exist.
    """
    file_path = Path(file_path)  # Ensure it's a Path object
    if not file_path.is_file():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with file_path.open("r", encoding="utf-8") as file:
        text = file.read()

    letters = "а-щьюяґєії" if LANGUAGE == 'uk' else 'a-z'
    pattern = f"[^{letters}\\s]"

    text = text.lower()
    text = re.sub(pattern, "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


def entropy_bound(text: str, alphabet: str, ngram_order: int) -> str:
    """
    Calculate entropy and verify the inequality for a given n-gram order.

    :param text: Input text.
    :param alphabet: The alphabet of the text.
    :param ngram_order: The n-gram order.
    :return: A formatted inequality string.
    """
    ngram_frequencies = calc_ngram_freq(text, ngram_order)

    h_n = calc_entropy(ngram_frequencies)

    alphabet_size = len(alphabet)
    min_entropy = math.log2(alphabet_size)
    max_entropy = ngram_order * min_entropy

    return f"{min_entropy:.4f} < H({ngram_order}) = {h_n:.4f} < {max_entropy:.4f}"


def analyze_text(
        directory: str,
        alphabet: str,
        lang_code: str = None
):
    """
    Analyze a text to calculate letter and bigram frequencies, entropy, and redundancy.

    :param directory: Path to the text file.
    :param alphabet: The alphabet used in the text.
    :param lang_code: The language code if filter is needed.
    :return: A dictionary with frequencies, entropy, and redundancy data.
    """
    results = []
    files = sorted(Path(directory).glob('*.txt'))

    alphabet_size = len(alphabet)

    for file in files:
        file_lang_code = file.stem[:2]

        if lang_code and file_lang_code != lang_code:
            print(f'[DEBUG] File {file} is not in {lang_code}. Skipping it...')
            continue

        text = load_text(file)

        general_entropy = compute_entropies(text)

        letter_freq = calc_freq(text)
        bigram_freq = calc_bigram_freq(text)

        letter_entropy = calc_entropy(letter_freq)  # H_1
        bigram_entropy = calc_entropy(bigram_freq)  # H_2

        letter_redundancy = calc_redundancy(letter_entropy, alphabet_size)
        bigram_redundancy = calc_redundancy(bigram_entropy, alphabet_size, True)

        bounds: dict = {
            n: entropy_bound(text, alphabet, n)
            for n in [10, 20, 30]
        }

        redundancy = calc_langauge_redundancy(bounds, alphabet_size)

        results.append({
            "file": file.name,
            "lang_code": file_lang_code,
            "letter_frequencies": letter_freq,
            "bigram_frequencies": bigram_freq,
            "letter_entropy": letter_entropy,
            "bigram_entropy": bigram_entropy,
            "letter_redundancy": letter_redundancy,
            "bigram_redundancy": bigram_redundancy,
            "entropy": general_entropy,
            "bounds": bounds,
            "redundancy": redundancy
        })

    return results


def compute_entropies(text: str) -> dict[str, float]:
    """
    Compute the required entropies.

    :param text: Input text.
    :return: A dictionary of entropy values.
    """
    text_strip = text.replace(" ", "")

    letters_1 = calc_freq(text)  # letters, with spaces
    letters_0 = calc_freq(text_strip)     # letters, without spaces

    bigrams_1_1 = calc_bigram_freq(text, crossing=True)  # with spaces + crossing
    bigrams_1_0 = calc_bigram_freq(text, crossing=False)  # with spaces + no crossing

    bigrams_0_1 = calc_bigram_freq(text_strip, crossing=True)  # no spaces + crossing
    bigrams_0_0 = calc_bigram_freq(text_strip, crossing=False)  # no spaces + no cross

    return {
        "Letters w/ spaces": calc_entropy(letters_1),
        "Letters no spaces": calc_entropy(letters_0),
        "Bigrams w/ spaces (crossing)": calc_entropy(bigrams_1_1),
        "Bigrams w/ spaces (no crossing)": calc_entropy(bigrams_1_0),
        "Bigrams no spaces (crossing)": calc_entropy(bigrams_0_1),
        "Bigrams no spaces (no crossing)": calc_entropy(bigrams_0_0),
    }


def calc_langauge_redundancy(bounds: dict[int, str], alphabet_size: int)-> dict[int, float]:
    """
    Calculate redundancy for a language based on observed entropy values and
    theoretical bounds.

    :param bounds: A dictionary of entropy bounds for different n-grams
    :param alphabet_size: The size of the alphabet.
    :return: The redundancy dictionary for each n-gram order.
    """
    redundancy = {}

    for n, bound in bounds.items():
        parts = bound.split("<")
        h_obs = float(parts[1].split("=")[1].strip())
        h_max = float(parts[2].strip())

        r = 1 - (h_obs / h_max)
        redundancy[n] = r

    return redundancy


def generate_report(
        results: list[dict],
        aggregated: dict,
        output_path: str,
        alphabet: str,
) -> None:
    """Generate text report."""
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    num_files = len(results)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("Text analysis:\n")
        file.write(f"Date: {report_date}\n")
        file.write(f"No. of Files: {num_files}\n")
        file.write("\n")

        for result in results:
            file.write(f"File: {result['file']}\n")
            file.write(f"Language: {result['lang_code']}\n")
            file.write(f"Letters Entropy: {result['letter_entropy']:.4f}\n")
            file.write(f"Bigrams Entropy: {result['bigram_entropy']:.4f}\n")
            file.write(f"Letters Redundancy: {result['letter_redundancy']:.4f}\n")
            file.write(f"Bigrams Redundancy: {result['bigram_redundancy']:.4f}\n")
            file.write(f"Detailed Entropy:\n")
            for key, value in result['entropy'].items():
                is_bigram = 'Bigram' in key
                file.write(f'\t{key}:'
                           f'\n\t\tEntropy: {value:.4f}'
                           f'\tRedundancy:{calc_redundancy(value, len(alphabet), is_bigram)}\n')
            file.write(f"Bounds:\n")
            for key, value in result['bounds'].items():
                file.write(f'\tN = {key}: {value}\n')
            file.write(f"Language Redundancy:\n")
            for key, value in result['redundancy'].items():
                file.write(f'\tN = {key}: R ~= {value:.4f}\n')
            file.write("\n")

        file.write("Aggregated results:\n")
        file.write(
            f"AVG Letters Entropy: {aggregated['average_letter_entropy']:.4f}\n"
        )
        file.write(
            f"AVG Bigrams Entropy: {aggregated['average_bigram_entropy']:.4f}\n"
        )
        file.write(
            f"AVG Letters Redundancy: {aggregated['average_letter_redundancy']:.4f}\n"
        )
        file.write(
            f"AVG Bigrams Redundancy: {aggregated['average_bigram_redundancy']:.4f}\n"
        )


def aggregate_results(results: list[dict]) -> dict:
    """
    Aggregate results from all files.

    :param results: Result list for each file
    :return: Aggregated dictionary.
    """
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    num_files = len(results)
    if num_files == 0:
        return {}

    total_letter_frequencies = Counter()
    total_bigram_frequencies = Counter()
    total_letter_entropy = 0
    total_bigram_entropy = 0
    total_letter_redundancy = 0
    total_bigram_redundancy = 0

    for result in results:
        total_letter_frequencies.update(result.get("letter_frequencies", {}))
        total_bigram_frequencies.update(result.get("bigram_frequencies", {}))

        total_letter_entropy += result["letter_entropy"]
        total_bigram_entropy += result["bigram_entropy"]
        total_letter_redundancy += result["letter_redundancy"]
        total_bigram_redundancy += result["bigram_redundancy"]

    total_letters = sum(total_letter_frequencies.values())
    total_bigrams = sum(total_bigram_frequencies.values())
    normalized_letter_frequencies = {k: v / total_letters for k, v in
                                     total_letter_frequencies.items()}
    normalized_bigram_frequencies = {k: v / total_bigrams for k, v in
                                     total_bigram_frequencies.items()}

    return {
        "data": report_date,
        "num_files": num_files,
        "average_letter_entropy": total_letter_entropy / num_files,
        "average_bigram_entropy": total_bigram_entropy / num_files,
        "average_letter_redundancy": total_letter_redundancy / num_files,
        "average_bigram_redundancy": total_bigram_redundancy / num_files,
        "normalized_letter_frequencies": normalized_letter_frequencies,
        "normalized_bigram_frequencies": normalized_bigram_frequencies,
    }


def save_results(data: dict, output_path: str) -> None:
    """Save data into json."""
    with open(output_path, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_analysis(file_path: str) -> dict:
    """
    Load analysis file.

    :param file_path: Path to the file.
    :return: Dictionary
    """
    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(f"File '{file_path}' not found.")

    if file.suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    else:
        raise ValueError(f"Not supported file format: {file.suffix}")


def main():
    """Entry point."""
    directory: str = './texts'
    alphabet: str = ALPHABET_UK if LANGUAGE == 'uk' else ALPHABET_EN

    results = analyze_text(directory, alphabet, lang_code=LANGUAGE)
    aggregated = aggregate_results(results)

    generate_report(results, aggregated, f'report_{LANGUAGE}.txt', alphabet)
    save_results(aggregated, f'./analysis_{LANGUAGE}.json')


if __name__ == "__main__":
    main()
