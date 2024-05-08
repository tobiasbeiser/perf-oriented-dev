import sys
import json
import csv
import os

def generate_csv(directory):
    output_file = 'output.csv'
    data = {}
    values=['1', '8', '32', '64', '256', '1024', '4096']
    for width in values:
        data[width] = {}
        for height in values:
            data[width][height] = None
        
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                json_data = json.load(file)
                real_time = json_data['results']['real']
                width = json_data['width']
                height = json_data['height']
                data[width][height] = real_time
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Width/Height'] + values)
        for width in values:
            row_data = [width] + [str(data[width][height]).replace('.', ',') if data[width][height] is not None else '' for height in values]
            writer.writerow(row_data)

    print("Data has been written to", output_file)



def main():
    if len(sys.argv) != 2:
        print("Usage: python {} <directory>".format(argv[0]))
        sys.exit(1)

    res_dir = sys.argv[1]
    generate_csv(res_dir)


if __name__ == "__main__":
    main()
