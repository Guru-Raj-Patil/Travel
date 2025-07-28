import urllib.request
import re

html = (
    urllib.request.urlopen("https://www.youtube.com/results?search_query=spark+plate")
    .read()
    .decode("utf-8")
)

# extract ytInitialData and dump it into a json file
ytInitialData = re.search(r"var ytInitialData = ({.*?});", html).group(1)

# Open file with UTF-8 encoding
with open("ytInitialData.json", "w", encoding="utf-8") as f:
    f.write(ytInitialData)
