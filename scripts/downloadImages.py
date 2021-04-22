import csv
import requests
import sys
import time
from tqdm import tqdm

imageFile = '/data/images.csv'
outputFolder = '/images'

maxRetries = 3

offset = int(sys.argv[1]) if len(sys.argv) >= 2 else 0
limit = int(sys.argv[2]) if len(sys.argv) >= 3 else 999999

data = []

with open(imageFile, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

for row in tqdm(data[offset:offset + limit]):
    id = row['id'][len("https://resource.swissartresearch.net/artwork/"):]
    url = row['image']
    outputFile = '%s/%s.tif' % (outputFolder, id)
    r = requests.get(url, allow_redirects=True)
    retries = 1
    while not 'image' in r.headers['Content-Type'] and retries <= maxRetries:
        # Try again if no image comes back
        time.sleep(1)
        r = requests.get(url, allow_redirects=True)
        retries += 1

    if retries >= maxRetries:
        print("Could not download", id, url)
    else:
        with open(outputFile, 'wb') as f:
            f.write(r.content)
