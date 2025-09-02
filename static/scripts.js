
async function askAI(){
  const input=document.getElementById('ai-question'); const out=document.getElementById('ai-answer');
  const q=(input.value||'').trim(); if(!q){out.textContent='Please type a question.';return;}
  out.textContent='Thinking...';
  try{
    const res=await fetch('/ask_ai',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
    const data=await res.json(); out.textContent=data.answer||data.error||'No response';
  }catch(e){out.textContent='Error contacting AI service.';}
}
async function balanceEq(){
  const input=document.getElementById('eq-input'); const out=document.getElementById('eq-output');
  const eq=(input.value||'').trim(); if(!eq){out.textContent='Enter equation (e.g., H2 + O2 -> H2O)';return;}
  out.textContent='Balancing...';
  try{
    const res=await fetch('/balance',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({equation:eq})});
    const data=await res.json(); out.textContent=data.balanced||data.error||'No response';
  }catch(e){out.textContent='Error balancing equation.';}
}
