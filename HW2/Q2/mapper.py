import sys
import csv

def mapper(file_path):
    results = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            artist = row[2]
            duration = row[3]
            results.append((artist, float(duration)))
    return results
