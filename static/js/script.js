document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM READY");

    const toggleBtn = document.getElementById("darkToggle");

    if (!toggleBtn) {
        console.log("Button not found");
        return;
    }

    toggleBtn.addEventListener("click", () => {
        console.log("CLICKED");

        document.body.classList.toggle("dark-mode");

        localStorage.setItem(
            "theme",
            document.body.classList.contains("dark-mode") ? "dark" : "light"
        );
    });

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
});