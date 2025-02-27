async function connectGET(){
  let username=document.getElementById('username').value;
  let response=await fetch(`/api/member?username=${username}`, {
    method:"GET"
  });
  let data=await response.json();

  const container = document.getElementById('SearchResult');

  if (data.data) {
    container.textContent=`${data.data.name} (${data.data.username})`;
  }else{
    container.textContent="查無此人"
  }
}

async function updateName() {
  let newname = document.getElementById('newname').value;
  let response = await fetch('/api/member', {
    method:"PATCH",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "name": newname })
  });
  let data = await response.json();

  const container = document.getElementById('UpdateResult');

  if (data) {
    container.textContent="更新成功";
  }
}