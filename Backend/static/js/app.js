console.log("HOSTEL SCOUT Loaded Successfully");

// ================================
// Hostel Gallery Slider
// ================================

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".gallery").forEach(gallery => {

        const images = gallery.querySelectorAll(".gallery-image");
        const prev = gallery.querySelector(".gallery-prev");
        const next = gallery.querySelector(".gallery-next");
        const current = gallery.querySelector(".current");

        if (images.length <= 1) return;

        let index = 0;

        function showImage(i) {

            images.forEach(img => img.classList.remove("active"));

            images[i].classList.add("active");

            if (current) {
                current.textContent = i + 1;
            }
        }

        next.addEventListener("click", (e) => {
            e.preventDefault();

            index++;

            if (index >= images.length) {
                index = 0;
            }

            showImage(index);
        });

        prev.addEventListener("click", (e) => {
            e.preventDefault();

            index--;

            if (index < 0) {
                index = images.length - 1;
            }

            showImage(index);
        });

        showImage(index);

    });

});