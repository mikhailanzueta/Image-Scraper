from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import zipfile, requests, io, os, json, time
from scraper import scrape_image_urls, download_and_zip

app = Flask(__name__)
CORS(app) 

@app.route("/", methods=["GET"])
def index():
    return "<h1>Reddit Image Scraper is Running</h1>"

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    url = data.get('url')
    subreddit = data.get('subreddit')
    num_of_images = data.get('numImages')

    try:
        number_of_images = min(int(num_of_images), 100)
    except (ValueError, TypeError):
        return jsonify({'error': "Invalid number of images"}), 400

    if not url or not subreddit:
        return jsonify({"error: Missing URL in request body"}), 400

    print(f"Scraping {number_of_images} images from: {url}")

    try:
        image_urls = scrape_image_urls(url, number_of_images)
        zip_buffer = download_and_zip(image_urls)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='images.zip'  # Flask 2.0+
        )
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500
    
    
@app.route("/download-images", methods=['POST'])
def download_images(request):
    data = request.get_json()
    image_urls = data.get('image_urls', [])
    zip_buffer = download_and_zip(image_urls)

    for image in request:
        download_and_zip(image_urls)

        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='images.zip'
        )
        
if __name__ == "__main__":
    app.run(host="localhost")
