import re
import json

def sanitize_and_validate(request_body):
    try:
        data = json.loads(request_body)

        # Extract and validate fields
        url = data.get('url', '').strip()
        number_of_images = data.get('number_of_images')

        # Basic validation
        if not url or not isinstance(number_of_images, int):
            return {"error": "Missing or invalid fields."}, 400
        
        if not re.match(r"^https?://(www\.)?reddit\.com/r/[a-zA-Z0-9_]+/?", url):
            return {"error": "Invalid subreddit url"}, 400
        
        if number_of_images < 1 or number_of_images > 100:
            return {"error": "Number of images must be between 1 and 100"}, 400
        
        # Extract and sanitize subreddit
        match = re.search(r"reddit\.com/r/([a-zA-Z0-9_]+)", url)

        if not match:
            return {"error": "Subreddit not found in url"}, 400
        
        subreddit = match.group(1)
        sanitized_subreddit = re.sub(r"[^\w]", "", subreddit)

        return {"message": f"Scraping r/{sanitized_subreddit} for {number_of_images} images"}, 200

    except json.JSONDecodeError:
        return {"error": "Invalid JSON payload."}, 400