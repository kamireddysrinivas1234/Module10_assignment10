
const a=document.getElementById("a"),b=document.getElementById("b"),op=document.getElementById("op"),
btn=document.getElementById("btn"),result=document.getElementById("result");
btn.addEventListener("click",async()=>{result.textContent="…";try{const resp=await fetch("/api/calc",{method:"POST",
  headers:{"Content-Type":"application/json"},body:JSON.stringify({a:Number(a.value),b:Number(b.value),op:op.value})});
  const data=await resp.json();result.textContent=resp.ok?data.result:`Error: ${data.detail||resp.statusText}`}catch(e){result.textContent=`Error: ${e.message}`}});
// Users
const uu=document.getElementById("u_username"), ue=document.getElementById("u_email"), up=document.getElementById("u_password"),
ub=document.getElementById("u_btn"), uo=document.getElementById("u_out");
async function refreshUsers(){ const r=await fetch('/api/users'); uo.textContent=JSON.stringify(await r.json(), null, 2); }
ub.addEventListener('click', async ()=>{
  const r = await fetch('/api/users', { method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({username: uu.value, email: ue.value, password: up.value}) });
  if(!r.ok){ const e = await r.json(); alert(e.detail || r.statusText); } await refreshUsers();
});
refreshUsers();
