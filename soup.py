#beautiful soup functions for parsing web pages

from bs4 import BeautifulSoup

#BS boilerplate
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())
