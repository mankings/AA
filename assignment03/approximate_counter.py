import click
import random
import math
import string

def approximate_counter(input_file, output_file=None):
    """
    This function reads a text file and counts the occurrences of each letter using Decreasing Probability Counter.
    """
    if output_file is None: output_file = input_file.replace('.txt', '_approximate.txt')
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        # Initialize counters for each letter
        counts = {letter: 0 for letter in string.ascii_uppercase}
        probabilities = {letter: 1.0 for letter in string.ascii_uppercase}

        # Process each letter in the text
        for char in text:
            if char in counts:
                # Update the count with decreasing probability
                if random.random() < probabilities[char]:
                    counts[char] += 1
                    probabilities[char] = 1 / math.sqrt(2) ** counts[char]

        # Writing approximate counts to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for letter, count in counts.items():
                f.write(f"{letter}: {count}\n")

        print(f"Approximate counts saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def approximate_counter_cli(input_file):
    approximate_counter(input_file)

if __name__ == "__main__":
    approximate_counter_cli()
