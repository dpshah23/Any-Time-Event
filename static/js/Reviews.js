document.addEventListener("DOMContentLoaded", function() {
    const readMoreLinks = document.querySelectorAll(".read-more");

    readMoreLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const reviewTextElement = event.target.closest(".review-text");
            const fullText = reviewTextElement.getAttribute("data-full-text");
            reviewTextElement.innerHTML = fullText;
        });
    });
});
