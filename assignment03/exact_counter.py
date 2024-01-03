import click
import string

def exact_counter(input_file, output_file=None):
    """
    This function reads a text file, counts the occurrences of each letter, and saves the counts to an output file.
    """
    if output_file is None: output_file = input_file.replace('.txt', '_exact.txt')
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        # Initialize a dictionary to count each letter
        letter_counts = {letter: 0 for letter in string.ascii_uppercase}

        # Manually count each letter
        for char in text:
            if char in letter_counts:
                letter_counts[char] += 1

        # Writing counts to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for letter, count in letter_counts.items():
                f.write(f"{letter}: {count}\n")

        print(f"Letter counts saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def exact_counter_cli(input_file):
    exact_counter(input_file)

if __name__ == "__main__":
    exact_counter_cli()
