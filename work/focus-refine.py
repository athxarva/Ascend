from pathlib import Path
p=Path('ascend/dist/index.html');s=p.read_text().replace('style.css?v=2','style.css?v=3').replace('app.js?v=2','app.js?v=3')
s=s.replace('<main><div class="dashboard">','<main><div class="page-intro"><h1 id="pageHeadline">Make room for <em>progress.</em></h1></div><div class="dashboard">')
s=s.replace('<span class="quote-star">✳</span>','<span class="quote-star">✳</span>')
s=s.replace('<div class="hours-bottom">','<div id="focusWeek" class="focus-week" aria-label="Focus minutes this week"></div><div class="hours-bottom">')
s=s.replace('<div class="toast" id="toast"', '''<section id="focusScreen" class="focus-screen" role="dialog" aria-modal="true" aria-label="Focus session" hidden><button id="leaveFocus" class="focus-back" aria-label="Return to dashboard">↗</button><div class="immersive-content"><div class="immersive-ring" id="immersiveRing"><div id="immersiveTimer" role="timer">25:00</div></div><blockquote id="immersiveQuote"></blockquote><div class="immersive-controls"><button id="immersivePause">Pause</button><button id="immersiveFinish">Finish session</button></div></div></section><div class="toast" id="toast"''')
p.write_text(s)
p=Path('ascend/dist/app.js');s=p.read_text()
s=s.replace("function startTimer(){let s=selection();", "function startTimer(){const origin=$('startTimer')?.getBoundingClientRect();let s=selection();")
s=s.replace('prepared=null;save();renderFocus();}\nfunction accrue()', 'prepared=null;save();renderFocus();enterFocus(origin);}\nfunction accrue()')
s=s.replace("function showFinish(){const s=state.active;", "function showFinish(){leaveFocus();const s=state.active;")
s=s.replace("$('timerRing').classList.toggle('paused',active?.status==='paused');", "$('timerRing').classList.toggle('paused',active?.status==='paused');updateTimerVisual(secs,active?.total||s?.remaining||1500);$('immersivePause').textContent=active?.status==='paused'?'Resume':'Pause';")
s=s.replace("$('focusSecondary').innerHTML=active?'':", "$('focusSecondary').innerHTML=active&&active.status!=='ended'?'<button id=\"enterFocus\">Enter focus view</button>':active?'':")
s=s.replace("if($('startTimer'))$('startTimer').onclick=startTimer;", "if($('enterFocus'))$('enterFocus').onclick=()=>enterFocus();if($('startTimer'))$('startTimer').onclick=startTimer;")
s=s.replace("function tick(){const now=", "function tick(){rotateCopy();const now=")
s=s.replace("const seconds=remainingSeconds(state.active);$('timer').textContent=", "const seconds=remainingSeconds(state.active);updateTimerVisual(seconds,state.active.total);$('timer').textContent=")
s=s.replace("$('hoursGoal').textContent=id?goalName(id):'your goals';", """$('hoursGoal').textContent=id?goalName(id):'your goals';const week=Array.from({length:7},(_,i)=>{const d=new Date();d.setDate(d.getDate()-6+i);return {label:d.toLocaleDateString(undefined,{weekday:'short'}),minutes:Math.round(sessions.filter(s=>s.date===dayKey(d)).reduce((n,s)=>n+s.seconds,0)/60)};});const peak=Math.max(30,...week.map(d=>d.minutes));$('focusWeek').innerHTML=week.map(d=>`<div title="${d.label}: ${d.minutes} minutes"><i style="height:${Math.max(3,d.minutes/peak*100)}%"></i><span>${d.label[0]}</span></div>`).join('');""")
a=s.index('const quotes=')
s=s[:a]+'''const quotes=["Make room for progress.","One small step is still a step forward.","Give this moment your attention.","Start where you are. Keep moving.","Progress grows with practice.","You don’t need to do it all today.","A little focus. A little closer.","Let the next step be enough."];
const headlines=['Make room for <em>progress.</em>','A little closer to <em>your goal.</em>','Small steps. Real <em>momentum.</em>','Give your goals a little <em>space.</em>'];
let copySlot=-1;
function rotateCopy(){const slot=Math.floor(Date.now()/180000);if(slot===copySlot)return;copySlot=slot;const quote=quotes[slot%quotes.length];$('quote').textContent=quote;$('immersiveQuote').textContent=quote;}
function updateTimerVisual(seconds,total){const ratio=Math.max(0,Math.min(1,seconds/Math.max(1,total)));$('timerRing').style.setProperty('--remaining',ratio);$('immersiveRing').style.setProperty('--remaining',ratio);$('immersiveTimer').textContent=`${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`;}
let focusReturn=null;
function enterFocus(origin){if(!state.active||state.active.status==='ended')return;focusReturn=document.activeElement;const screen=$('focusScreen');screen.hidden=false;document.querySelector('.app-shell').inert=true;document.body.classList.add('immersed');const x=origin?origin.left+origin.width/2:innerWidth/2,y=origin?origin.top+origin.height/2:innerHeight/2;const radius=Math.hypot(Math.max(x,innerWidth-x),Math.max(y,innerHeight-y));if(!matchMedia('(prefers-reduced-motion: reduce)').matches)screen.animate([{clipPath:`circle(0px at ${x}px ${y}px)`},{clipPath:`circle(${radius}px at ${x}px ${y}px)`}],{duration:650,easing:'cubic-bezier(.22,.8,.2,1)'});$('immersivePause').focus({preventScroll:true});}
function leaveFocus(){if($('focusScreen').hidden)return;$('focusScreen').hidden=true;document.querySelector('.app-shell').inert=false;document.body.classList.remove('immersed');if(focusReturn?.isConnected)focusReturn.focus({preventScroll:true});else $('pauseTimer')?.focus({preventScroll:true});}
$('leaveFocus').onclick=leaveFocus;$('immersivePause').onclick=togglePause;$('immersiveFinish').onclick=endCheckIn;
$('focusScreen').addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();leaveFocus();}if(e.key==='Tab'){const buttons=[$('leaveFocus'),$('immersivePause'),$('immersiveFinish')];const index=buttons.indexOf(document.activeElement);if((e.shiftKey&&index===0)||(!e.shiftKey&&index===2)){e.preventDefault();buttons[e.shiftKey?2:0].focus();}}});
document.querySelectorAll('select').forEach(select=>enhanceSelect(select,select.id==='goalFilter'?{footerLabel:'Manage goals',onFooter:openGoals}:{}));
$('pageHeadline').innerHTML=headlines[Math.floor(Math.random()*headlines.length)];rotateCopy();render();if(state.active?.status==='ended')showFinish();tick();setInterval(tick,1000);if(state.demo)toast("You're exploring a sample day.");if(storageError)toast('Saved data could not be read. Your previous storage has not been overwritten.');
'''
p.write_text(s)
