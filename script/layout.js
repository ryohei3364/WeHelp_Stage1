function toggleMenu() {
    var menu = document.querySelector('.menu');
    var close = document.querySelector('.mobile-close'); 
    var mobileMenu = document.querySelector('.mobile-menu');

    // 檢查menu是否為隱藏或未設定display屬性
    if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "flex"; // 顯示menu選單
        close.style.display = "block"; // 顯示close按鈕
        mobileMenu.style.display = "none"; // 隱藏menu按鈕
    } else {
        menu.style.display = "none"; // 隱藏menu選單
        close.style.display = "none"; // 隱藏close按鈕
        mobileMenu.style.display = "block"; // 顯示menu按鈕
    }
}