import requests # to make http requests
from bs4 import BeautifulSoup # to parse the http response
import os # to create a new directory to store the downloaded qp

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}

# requesting the url for a response

#### uncomment any one of the urls

# for DBMS
# url = 'https://www.ktuqbank.com/2020/03/principles-database-design-cs208-question-papers.html'
# for OS
# url = 'https://www.ktuqbank.com/2020/03/operating-systems-cs204-question-papers.html'
# for COA
url = 'https://www.ktuqbank.com/2020/03/computer-organisation-architecture-cs202-question-papers.html' 

try:
    response = requests.get(url, headers=headers)
    print("Received response from server...")
except requests.exceptions.ConnectTimeout:
    print("Error! Request timed out!")
    raise SystemExit()
except requests.exceptions.HTTPError:
    print("An HTTP error occurred")
    raise SystemExit()
except requests.exceptions.TooManyRedirects:
    print("Bad URL! Please check your URL again!")
    raise SystemExit()
except:
    print("Please check your connection!")
    raise SystemExit()

# parsing the received response
try:
    response = BeautifulSoup(response.content, 'html.parser')
    print("Successfully parsed the content...")
except:
    print("Error while parsing response.")
    raise SystemExit()

tab_content = response.find_all("div", class_="tabcontent")
for content in tab_content:
    pdfs = content.find_all("a", class_="maxbutton-226", href=True)
result = [a['href'] for a in pdfs if a.text]  # works only if anchor tag has a text

# replace path/to/directory with your own path
print("Creating directory... <path/to/directory>")
try:
    os.mkdir('<path/to/directory>')
except OSError as err:
    print("Directory exists")

# retreiving links and downloading
print("Retreiving links...")
print("Initialising downloads...\n")
count = 0
for download_url in result:
    count += 1
    print(f"Downloading pdf {count}")
    to_download = requests.get(download_url)
    try:
        pdf = open(f"<path/to/directory>/qp{count}.pdf", "wb")
    except:
        print("Error while writing into file")
        raise SystemExit(1)
    pdf.write(to_download.content)
    pdf.close()

print("Done!")