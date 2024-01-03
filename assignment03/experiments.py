import click
import os
import glob

from exact_counter import exact_counter
from approximate_counter import approximate_counter
from data_stream import space_saving_counter

@click.command()
@click.argument('folder_path', default="gutenberg", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('output_path', default="results", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('runs', default=5, type=int)
def process_folder(folder_path, output_path, runs):
    """
    Processes each .txt file in the specified folder using Exact Counter, Approximate Counter, and Space-Saving Counter algorithms.
    """
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    for file in txt_files:
        if file.endswith('_clean.txt'):
            print(f"Processing {file}...")
            out = file.replace(folder_path, output_path).replace("_clean.txt", "") + "/" + os.path.basename(file).replace("_clean.txt", "")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            
            exact_counter(file, out + "_exact.txt")
            for i in range(runs): approximate_counter(file, out + f"_approx_{i}.txt")
            space_saving_counter(file, 3, out + f"_space_saving3.txt")
            space_saving_counter(file, 5, out + f"_space_saving5.txt")
            space_saving_counter(file, 10, out + f"_space_saving10.txt")

            print(f"Finished processing {file}")


if __name__ == '__main__':
    process_folder()