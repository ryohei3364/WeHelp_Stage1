function checked(event){
  event.preventDefault(); 
  let checkbox = document.querySelector("#check");
  if (!checkbox.checked){
    alert("請勾選同意條款");
  } else {
    event.target.submit();
  }
}
let signin = document.querySelector("#signin");
signin?.addEventListener("submit", checked);


function redirectToSquare(event){
  event.preventDefault();
  let num = parseInt(document.getElementById("num").value);
  if (!Number.isInteger(num) || num <= 0) {
    alert("請填入正整數");
  } else {
    window.location.href = `/square/${num}`;
  }
}