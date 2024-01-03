import click
import heapq
import string

class SpaceSavingCounter:
    def __init__(self, size):
        self.size = size
        self.counters = {}
        self.min_heap = []

    def process(self, item):
        if item in self.counters:
            self.counters[item][0] += 1
            heapq.heapify(self.min_heap)
        elif len(self.min_heap) < self.size:
            self.counters[item] = [1, item]
            heapq.heappush(self.min_heap, self.counters[item])
        else:
            min_item = heapq.heappop(self.min_heap)
            del self.counters[min_item[1]]
            self.counters[item] = [min_item[0] + 1, item]
            heapq.heappush(self.min_heap, self.counters[item])

    def get_top_items(self):
        return sorted([(item, count[0]) for item, count in self.counters.items()], key=lambda x: -x[1])

def space_saving_counter(input_file, n, output_file=None):
    """
    This function reads a text file and identifies the n most frequent letters using Space-Saving algorithm.
    """
    if output_file is None: output_file = input_file.replace('.txt', f'_stream_{n}.txt')
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        # Initialize the SpaceSavingCounter
        counter = SpaceSavingCounter(n)

        # Process each letter in the text
        for char in text:
            if char in string.ascii_uppercase:
                counter.process(char)

        # Writing results to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for letter, count in counter.get_top_items():
                f.write(f"{letter}: {count}\n")

        print(f"Top {n} letter counts saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--n', default=10, help='Number of top items to find.')
def space_saving_counter_cli(input_file, n):
    space_saving_counter(input_file, n)


if __name__ == "__main__":
    space_saving_counter_cli()
