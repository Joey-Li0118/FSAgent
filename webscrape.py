import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# The target URL
url = "https://www.fsa.usda.gov/news-events/laws-regulations/fsa-handbooks" 

# NEW: Add a User-Agent header to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. Fetch the page content with headers
try:
    # We add headers=headers here
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status() # This will catch 404s or 500s early
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # 2. Create a folder to save PDFs
    folder_name = "USDA_PDFs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 3. Find all <a> tags
    pdf_links = soup.find_all('a', href=True)

    print(f"Starting download...")

    for link in pdf_links:
        href = link['href']
        if href.lower().endswith('.pdf'):
            full_url = urljoin(url, href)
            
            # Get the link title, fall back to URL slug if no title
            title = link.get('title') or link.get_text(strip=True)
            if title:
                # Clean the title to make it a valid filename
                safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()
                filename = os.path.join(folder_name, safe_title + ".pdf")
            else:
                filename = os.path.join(folder_name, href.split('/')[-1])
            
            try:
                print(f"Downloading: {filename}")
                pdf_response = requests.get(full_url, headers=headers, timeout=20)
                with open(filename, 'wb') as f:
                    f.write(pdf_response.content)
            except Exception as e:
                print(f"Failed to download {full_url}. Error: {e}")
    print("Done!")

except requests.exceptions.RequestException as e:
    print(f"Connection Error: {e}")