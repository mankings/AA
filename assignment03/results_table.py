import os
import glob

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
            data.append([letter] + [float(v.split(': ')[1]) for v in values[0:3]])
    
    return data

def main():
    results_file = "analysis_results.txt"
    for folder in glob.glob("results/*"):
        results = ""
        with open(os.path.join(folder, results_file), 'r') as file:
            results = parse_results(file.read())

        with open(os.path.join(folder, "table.txt"), 'w') as file:
            # sort letters by all three metrics
            results.sort(key=lambda x: x[1], reverse=True)
            for line in results:
                file.write(str(line[0]) + " - " + str(line[1]) + '\n')
    
            results.sort(key=lambda x: x[2], reverse=True)
            file.write("---\n")
            for line in results:
                file.write(str(line[0]) + " - " + str(line[2]) + '\n')

            results.sort(key=lambda x: x[3], reverse=True)
            file.write("---\n")
            for line in results:
                file.write(str(line[0]) + " - " + str(line[3]) + '\n')
    
    data = {}
    for file in glob.glob("results/*/table.txt"):
        work = file.split("/")[1]
        with open(file, 'r') as f:
            temp = f.readlines()
            key = 0
            if key not in data: data[key] = {}
            if work not in data[key]: data[key][work] = []
                   
            for line in temp:
                if line.strip() == "---":
                    key += 1
                    if key not in data: data[key] = {}
                    if work not in data[key]: data[key][work] = []
                else:
                    data[key][work].append(line.strip())
    
    with open("results/data.txt", 'w') as file:
        for key in data.keys():
            if key == 0: algo = "Exact"
            if key == 1: algo = "Approx"
            if key == 2: algo = "Stream"
            file.write(str(algo) + '\n')
            for work in data[key].keys():
                file.write(str(work) + '\n')
                for line in data[key][work][0:10]:
                    file.write(str(line) + '\n')
                file.write('\n')

if __name__ == '__main__':
    main()


