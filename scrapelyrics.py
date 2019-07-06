#! python3
# AZLyrics Scrapper
# July 6, 2019

from requests import get
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from sys import argv


def print_error_and_exit(message):
    """
    Function for printing the error message then exiting.
    """
    print(message)
    exit()


# Form the title.
title = ' '.join(argv[1:])

# Search the song.
print('Searching for the song...')
try:
    response = get(f'https://search.azlyrics.com/search.php?q={title}')
except ConnectionError:
    print_error_and_exit('Oh. There was a connection problem.')

# Initialize the soup.
print('Parsing...')
soup = BeautifulSoup(response.content, 'html.parser')

# Exit if none was found.
if 'sorry, your search returned no results' in soup.body.get_text().lower():
    print('Your search returned none. Make sure that '
          'your query has correct spellings.')
    exit()

# Get the table that has the results.
table = None
for div in soup.find_all('div', attrs={'class': 'panel'}):
    if 'Song results:' in div.get_text():
        table = div.table
        break

# Skip the paginator and get the first link.
lyrics_link = ''
if table.tr.text.replace('\n', '') in '1234567':
    lyrics_link = table.find_all('tr')[1].td.a['href']
else:
    lyrics_link = table.tr.td.a['href']

# Get the lyrics.
print('Getting the lyrics found...')
try:
    response = get(lyrics_link)
except ConnectionError:
    print_error_and_exit(
        'Oh. Failed to get the lyrics due to '
        'connection problem.')

# Cook the soup.
print('Parsing...')
soup = BeautifulSoup(response.content, 'html.parser')

# Get the main div.
main_div = soup.select('div.col-xs-12.col-lg-8.text-center')[0]

# Form the lyrics.
found_title = main_div.find_all('div')[3].get_text()
lyrics = (
    # Title
    found_title +
    # Lyrics
    main_div.find_all('div')[6].get_text()
)

# Store the found lyrics in a txt file.
print('Writing the lyrics into a text file.')
with open(f'{found_title}.txt', 'w') as lyrics_txt_file:
    lyrics_txt_file.write(lyrics)

# Print the found lyrics.
print()
print(lyrics)
print()
print(f'{found_title} has been stored in a txt file.')
