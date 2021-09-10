import csv
import requests
import sys
import time
import os.path
from tqdm import tqdm

imageFileName = str(sys.argv[1]) # imagefile csv name
csvFolder = "/data/"
imageFile = os.path.join(csvFolder, imageFileName)
outputFolder = '/images'

maxRetries = 3

offset = int(sys.argv[2]) if len(sys.argv) >= 3 else 0
limit = int(sys.argv[3]) if len(sys.argv) >= 4 else 999999

data = []

with open(imageFile, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

for row in tqdm(data[offset:offset + limit]):
    id = row['id'].rsplit('/', 1)[-1] # takes the element after the last slash
    url = row['image']
    outputFile = '%s/%s.tif' % (outputFolder, id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'
    }
    if not url.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp', '.gif')): # check if the file is an image
            print(id,url,"is not an image")
    # Check if file exists
    elif not os.path.isfile(outputFile):
        r = requests.get(url, allow_redirects=True, headers=headers)
        retries = 1
        while not 'image' in r.headers['Content-Type'] and retries <= maxRetries:
            # Try again if no image comes back
            time.sleep(1)
            r = requests.get(url, allow_redirects=True, headers=headers)
            retries += 1

        
        if retries >= maxRetries:
            print("Could not download", id, url)
        
        else:
            with open(outputFile, 'wb') as f:
                f.write(r.content)
