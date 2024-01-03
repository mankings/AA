import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os

def parse_results(results):
    """
    Parses the results string into a pandas DataFrame.
    """
    data = []
    for line in results.split('\n'):
        if line:
            parts = line.split(' - ')
            letter = parts[0]
            values = parts[1].split(', ')
            data.append([letter] + [float(v.split(': ')[1]) for v in values])
    
    columns = ['Letter', 'Exact', 'Approx', 'Stream', 'Abs Error Approx', 'Rel Error Approx', 
               'Abs Error Stream', 'Rel Error Stream']
    return pd.DataFrame(data, columns=columns)

def plot_comparison(df, comparison_type='Exact-Approx', save_path='results'):
    """
    Plots the comparison between exact counts and approximate counts, or exact counts and data stream counts.
    """
    bar_width = 0.3
    index = np.arange(len(df))

    fig, ax1 = plt.subplots()

    if comparison_type == 'Exact-Approx':
        # Plotting the Exact counts on the primary y-axis
        ax1.bar(index, df['Exact'], bar_width, label='Exact', color='blue')
        ax1.set_xlabel('Letter')
        ax1.set_ylabel('Exact Count', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Create a second y-axis for the Approx counts
        ax2 = ax1.twinx()
        ax2.bar(index + bar_width, df['Approx'], bar_width, label='Approx', color='red')
        ax2.set_ylabel('Approx Count', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

    elif comparison_type == 'Exact-Stream':
        # Plotting the Exact and Stream counts on the primary y-axis
        ax1.bar(index, df['Exact'], bar_width, label='Exact', color='blue')
        ax1.bar(index + bar_width, df['Stream'], bar_width, label='Stream', color='green')
        ax1.set_xlabel('Letter')
        ax1.set_ylabel('Count')
        ax1.tick_params(axis='y')

    # Common elements for both types of comparison
    plt.title(f'Comparison between Exact Counts and {comparison_type.split("-")[1]} Counts')
    plt.xticks(index + bar_width / 2, df['Letter'])

    # Adding legends
    ax1_legend = ax1.legend(loc='upper right', bbox_to_anchor=(1, 1))
    if comparison_type == 'Exact-Approx':
        ax2_legend = ax2.legend(loc='upper right', bbox_to_anchor=(1, 0.94))


    plt.tight_layout()
    plt.savefig(f"{save_path}/{comparison_type}.png")
    plt.close(fig)


def main():
    results_file = "analysis_results.txt"
    for folder in glob.glob("results/*"):
        results = ""
        with open(os.path.join(folder, results_file), 'r') as file:
            results = file.read()
    
        df = parse_results(results)
        plot_comparison(df, comparison_type='Exact-Approx', save_path=f"{folder}")  # Plot for Exact vs Approx
        plot_comparison(df, comparison_type='Exact-Stream', save_path=f"{folder}")  # Plot for Exact vs Stream

if __name__ == '__main__':
    main()


