import requests
import urllib.request
import shutil
import re
import os

url = input('What is the url of the glossary section you want to scrape? ')

topic = url.split('/')[4]

dir = './output/lessons/' + topic

downloads = 0

if not os.path.exists(dir):
    os.makedirs(dir)
    print('Created directory:', dir)
else:
    print('Directory:', dir, 'Already exists, continuing...')

response = requests.get('https://www.persianlanguageonline.com/learn/nice-to-meet-you')

if response.status_code != 200:
    print('Failed to fetch content! Status Code:', response.status_code)
    quit()

print('Fetched content.')

lines = response.content.splitlines()

# TODO:
# Don't re-download mp3 files: duplicate check
# count mp3 downloads
for line in lines:
    parsedLine = str(line)
    if 'mp3: "' in parsedLine:
        parsedUrl = re.findall(r'"([^"]*)"', parsedLine)[0]
        mp3Name = parsedUrl.split('/')[7]

        fileDir = dir + '/' + mp3Name

        if not os.path.exists(fileDir):
            print('Found MP3 ' + mp3Name + ', downloading...')

            with urllib.request.urlopen(parsedUrl) as response, open(fileDir, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

            downloads += 1

print('Success! Downloaded', downloads, 'MP3 files.')