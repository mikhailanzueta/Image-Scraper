// Function to extract and validate form input
function getFormData() {
    const url = document.getElementById('url-input').value.trim();
    const numImages = parseInt(document.getElementById('number-input').value.trim(), 10);

    // Input validation
    if (!url || isNaN(numImages)) {
        throw new Error('Please fill out both form fields correctly.');
    }

    if (!/^https?:\/\/(www\.)?reddit\.com\/r\//.test(url)) {
        throw new Error('Please enter a valid Reddit subreddit URL.');
    }

    const match = url.match(/reddit\.com\/r\/([^\/]+)/);
    const subreddit = match ? match[1] : null;

    console.log("Subreddit:", subreddit);
    console.log("Number of images to scrape:", numImages);

    return {
        url: url,
        subreddit: subreddit,
        numImages: numImages
    };
}

// Function to send POST request and handle file download
async function sendScrapeRequest() {
    let formData;

    try {
        formData = getFormData();
    } catch (err) {
        console.error(err.message);
        alert(err.message);
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errResponse = await response.json();
            throw new Error(errResponse.error || 'Failed to download ZIP file.');
        }

        const blob = await response.blob();
        const blobUrl = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = 'images.zip';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(blobUrl);
    } catch (err) {
        console.error("Download error:", err.message);
        alert(`Error: ${err.message}`);
    }
}

// Event listener for form submission
document.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    sendScrapeRequest();
});
