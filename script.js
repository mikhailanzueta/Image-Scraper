// create a function that captures form elements
function form() {
    const url = document.querySelector('input[name="url"]')
    const number_of_imgs = document.querySelector('input[name="number"]');

    // check for empty input fields:
    if (!url || !number_of_imgs) {
        throw new Error('Please fill out the form field(s)')
    } else if (!url.includes("http://www.reddit.com/r/") || !url.includes("https://www.reddit.com/r/")) {
        throw new Error('Please enter a valid reddit url.')
    }
    return {
        url: url,
        number_of_imgs: Number(number_of_imgs)
    }
}