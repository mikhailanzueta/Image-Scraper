from bs4 import BeautifulSoup
from selenium import webdriver
import asyncio
import aiohttp
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import zipfile, requests, io, os, json, time


# Option 1: Load the url content using a headless chrome browser and return the full HTML:
def scrape_image_urls(url, limit=100):
    print("Testing: ", url)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36"
    )
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    WebDriverWait(driver, 10).until(        # Wait for reddit post containers to load
        EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
    )

    limit = int(limit)
    results = [] # Where to store the image urls
    # endings = ('jpg', 'jpeg', 'png') # Define a tuple of potential image endings
    seen = set() # Prevents duplicates
    
    
    last_page_height = driver.execute_script("return document.body.scrollHeight")
    scroll_pause_time = 2
    while len(results) < limit:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        posts = soup.find_all("shreddit-post", attrs={"post-type": "image"}) ## Look for real post containers


        for post in posts:
            img_tags = post.find_all("img", src=True)
            for img in img_tags:
                src = img['src']
                src_lower = src.lower()
                print("Source: ")

                # Filter: image must be hosted on Reddit's preview or i.redd.it (not avatar, emoji, or ad)
                if (
                    ("preview.redd.it" in src_lower or "i.redd.it" in src_lower)
                    and not any(x in src_lower for x in ["emoji", "avatar", "external-preview", "media?url"])
                    and src not in seen
                ):
                    results.append(src)
                    seen.add(src)
                if len(results) >= limit:
                    break

        # scroll to load more content:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(scroll_pause_time)

        new_page_height = driver.execute_script("return document.body.scrollHeight")
        if new_page_height == last_page_height:
            print("reached end of page. There is no more content to load.")
            break
        last_page_height = new_page_height

    driver.quit()
    assert isinstance(results, list), f"'results' changed type to {type(results)}"
    print("Found posts: ", len(posts))
    print(f"Collected {len(results)} images")
    return results[:limit]

async def get_images(session, url, index):
    try:
        async with session.get(url) as response:
            content = await response
            if response.status == 200:
                print(f"Content: ", content)
                ext = url.split('.')[-1].split('?')[0]
                if ext.lower() not in ['jpg', 'jpeg', 'png']:
                    ext = 'jpg'
                filename = f"image_{index + 1}.{ext}"
                print(f"Fetched: {filename}")
                return filename, content
    except Exception as e:
        print(f"Error downloading {url}: {e}")


async def download_and_zip(image_urls):
    zip_buffer = io.BytesIO()

    async with aiohttp.ClientSession() as session:
        tasks = [get_images(session, url, index) for index, url in enumerate(image_urls)]
        results = await asyncio.gather(*tasks)
        print(f"results: ", results)
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for filename, content in results:
                if filename and content:
                    zip_file.writestr(filename, content)
        return results


