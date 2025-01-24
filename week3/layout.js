function toggleMenu() {
  var menu = document.querySelector('.menu');
  var close = document.querySelector('.mobile-close');
  var mobileMenu = document.querySelector('.mobile-menu');

  window.addEventListener('resize', function (event) {
    if (window.innerWidth >= 601) {
      menu.style.display = "inline-block"; // 顯示menu選單
    } else {
      menu.style.display = "none"; // 隱藏menu選單
      mobileMenu.style.display = "inline-block"; // 顯示menu按鈕  
    }
  }, true);

  // 檢查menu是否為隱藏或未設定display屬性
  if (menu.style.display === "none" || menu.style.display === "") {
    menu.style.display = "inline-block"; // 顯示menu選單
    close.style.display = "inline-block"; // 顯示close按鈕
    mobileMenu.style.display = "none"; // 隱藏menu按鈕
  } else {
    menu.style.display = "none"; // 隱藏menu選單
    close.style.display = "none"; // 隱藏close按鈕
    mobileMenu.style.display = "inline-block"; // 顯示menu按鈕
  }

}

// This function is aimed to parse tourist spots data from url, and render contents as HTML.
async function fetchData() {
  // 1. fetch data from url 
  let response = await fetch(
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
  );
  let result = await response.json();
  let data = result.data.results;

  return data
}

function arrangeData(data) {
  // 2. arrange titles and images into arrays
  let spotsTitles = [];
  let spotsImages = [];

  for (let i = 0; i < data.length; i++) {
    const regex = /(https?:\/\/\S+?\.(?:jpg|jpeg|png|gif))/gi;
    spotsTitles.push(data[i].stitle);
    spotsImages.push(data[i].filelist.match(regex));
  }
  return { spotsTitles, spotsImages };
}

async function updateBox(boxName, startIndex, endIndex) {
  try {
    let data = await fetchData(); // Wait for fetchData to resolve
    let { spotsTitles, spotsImages } = arrangeData(data);
    console.log(spotsTitles);

    // 3. update the data into small-box layout
    let box = document.querySelector(`.${boxName}`);
    let boxChildren = box.children;

    for (let i = startIndex; i < Math.min(data.length, endIndex); i++) {
      let img = document.createElement("img");
      img.className = "image";
      img.src = `${spotsImages[i][0]}`;
      img.alt = `${spotsTitles[i]}`;

      let span = document.createElement("span");
      span.appendChild(document.createTextNode(spotsTitles[i]));
      span.className = "span"

      let div = boxChildren[i - startIndex];
      // 保留 star-img 元素，清空其他內容
      let img_star = document.createElement("img");
      img_star.className = "star";
      img.src = ".public/star.svg";
      // 清空 div 的所有子元素
      while (div.firstChild) {
        div.removeChild(div.firstChild);
      }
      // 將 img 和 textNode 添加到 div
      div.appendChild(img);
      div.appendChild(img_star);
      div.appendChild(span);
    }

  } catch (error) {
    console.error(error);
  }
}

updateBox('small-box', 0, 3);
updateBox('big-box', 3, 13);