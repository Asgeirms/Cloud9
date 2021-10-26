function hide_div(elemID) {
    const html_div = document.getElementById(elemID);
    if (html_div.style.display === "none") {
        html_div.style.display = "block";
    } else {
        html_div.style.display = "none";
    }
}
