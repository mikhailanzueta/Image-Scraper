# Image-Scraper
# This reddit image scraper is a side-project that compliments my main project that I am working on (LockedIn).
# This project gives me practice with web scraping which is an essential function of my main project.


# May 19, 2025:
    # Added form action and removed the window location from being set to the zip_path after sending fetch request. This prevents an unintended redirect on submit.

# May 21, 2025:
    # I 'loosened' the image filtering form my scraper.py file by removing the 'endings' tuple. That way i am not filtering out valid images.

    # Put the user-agent before launching the browser instead of after. Selenium was already launching the browser before the user-agent was declared, which caused reddit to ignore my request.

# May 22, 2025:
    # Re-factored my download_zip function create a zip file in memory only using IO.Bytes and returning binary zip data. Then send the file to the browser using Flasks send_file

    # Created an endpoint to trigger the download of the zip file and return the zip buffer as a downloadable file.

    # Re-factored my javascript to not expect JSON from the backend and to receive the binary file and treat it as a blob. Then trigger the download.

    # Modified scrape function so that it uses send_file to send in memory zip buffer instead of return ing the zip path

# may 26, 2025:
# server needs to create a zip file in memory upon new requests
# make a separate request for each image 
# Then pass a reference to zip file

# import io
import zipfile

def downloader(target_file):
    # do your requests here
    # then pass it as data below
    with zipfile.ZipFile(target_file, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr(file_name, data.getvalue())


@app.route("/my-endpoint")
def my_method(req):
    zip_buffer = io.BytesIO()

    for image in req:
        downloader(zip_buffer)

    zip_buffer.seek(0)
    return send_file(zip_buffer, attachment_filename='filename.zip', as_attachment=True)