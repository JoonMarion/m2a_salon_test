document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");
    const icon = toggleBtn.querySelector("i");

    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");

        if (sidebar.classList.contains("collapsed")) {
            icon.classList.replace("bi-chevron-double-left", "bi-chevron-double-right");
        } else {
            icon.classList.replace("bi-chevron-double-right", "bi-chevron-double-left");
        }
    });
});
