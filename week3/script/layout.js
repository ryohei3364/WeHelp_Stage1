// Task 3: is aimed to parse tourist spots data from url, and render contents as HTML.
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
  // 3. upload html content with fetched data and remove the old content
  try {
    let data = await fetchData();
    let { spotsTitles, spotsImages } = arrangeData(data); 

    // update the data into box layout
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

      // remove all div elements
      let div = boxChildren[i - startIndex];
      while (div.firstChild) {
        div.removeChild(div.firstChild);
      }

      // 4. create new elements for stars after the div childelements all removed
      if (boxName == 'big-box') {
        // big-box layout create star icons
        let img_star = document.createElement("img");
        img_star.className = "star";
        img_star.src = "./public/icon/star.svg";

        // add img, star, textNode into div
        div.appendChild(img);
        div.appendChild(img_star);
        div.appendChild(span);
      } else {
        // // add ONLY img and textNode into div
        div.appendChild(img);
        div.appendChild(span);      
      }
    }
  } catch (error) {
    console.error(error);
  }
}

updateBox('small-box', 0, 3);
updateBox('big-box', 3, 13);


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