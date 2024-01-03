import os
import glob
import numpy as np

def parse_file(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    return {line.split(': ')[0]: int(line.split(': ')[1]) for line in data}

def calculate_errors(exact_counts, other_counts):
    letters = sorted(exact_counts.keys())
    exact_positions = {letter: i for i, letter in enumerate(sorted(letters, key=lambda x: exact_counts[x], reverse=True))}
    
    # Handle missing letters in other_counts by using a default value
    other_positions = {letter: i for i, letter in enumerate(sorted(letters, key=lambda x: other_counts.get(x, 0), reverse=True))}
    
    absolute_errors = {letter: abs(exact_positions[letter] - other_positions.get(letter, len(letters))) for letter in letters}
    relative_errors = {letter: absolute_errors[letter] / len(letters) for letter in letters}
    
    return absolute_errors, relative_errors

def process_work(work_dir):
    exact_file = glob.glob(os.path.join(work_dir, '*_exact.txt'))[0]
    approx_files = glob.glob(os.path.join(work_dir, '*_approx_*.txt'))
    stream_files = glob.glob(os.path.join(work_dir, '*_space_saving10*.txt'))

    exact_counts = parse_file(exact_file)
    all_approx_counts = [parse_file(f) for f in approx_files]
    all_stream_counts = [parse_file(f) for f in stream_files]

    avg_approx_counts = {letter: np.mean([counts.get(letter, 0) for counts in all_approx_counts]) for letter in exact_counts.keys()}
    avg_stream_counts = {letter: np.mean([counts.get(letter, 0) for counts in all_stream_counts]) for letter in exact_counts.keys()}

    avg_absolute_errors_approx, avg_relative_errors_approx = calculate_errors(exact_counts, avg_approx_counts)
    avg_absolute_errors_stream, avg_relative_errors_stream = calculate_errors(exact_counts, avg_stream_counts)

    return exact_counts, avg_approx_counts, avg_stream_counts, avg_absolute_errors_approx, avg_relative_errors_approx, avg_absolute_errors_stream, avg_relative_errors_stream

def write_results_to_file(work_dir, results):
    exact_counts, avg_approx_counts, avg_stream_counts, avg_absolute_errors_approx, avg_relative_errors_approx, avg_absolute_errors_stream, avg_relative_errors_stream = results
    sorted_letters = sorted(exact_counts.keys(), key=lambda x: exact_counts[x], reverse=True)
    with open(os.path.join(work_dir, 'analysis_results.txt'), 'w') as file:
        for letter in sorted_letters:
            file.write(f"{letter} - Exact: {exact_counts[letter]}, Approx: {avg_approx_counts[letter]:.2f}, Stream: {avg_stream_counts.get(letter, 0):.2f}, Abs Error Approx: {avg_absolute_errors_approx[letter]:.2f}, Rel Error Approx: {avg_relative_errors_approx[letter]:.2f}, Abs Error Stream: {avg_absolute_errors_stream.get(letter, len(sorted_letters)):.2f}, Rel Error Stream: {avg_relative_errors_stream.get(letter, 1.0):.2f}\n")

def main():
    # Path to the directory containing the results
    works_dir = 'results'
    for work_dir in glob.glob(os.path.join(works_dir, '*')):
        results = process_work(work_dir)
        write_results_to_file(work_dir, results)

if __name__ == '__main__':
    main()
