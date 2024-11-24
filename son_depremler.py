import requests
from bs4 import BeautifulSoup

url = "http://www.koeri.boun.edu.tr/scripts/lst8.asp"

response = requests.get(url)
content = response.content

soup = BeautifulSoup(content, "html.parser")

pre = soup.find("pre")
text = pre.text

liste = text.split("\n")

print("\n".join(liste[4:12]))
