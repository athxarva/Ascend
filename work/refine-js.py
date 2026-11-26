from pathlib import Path
p=Path('ascend/dist/app.js');s=p.read_text()
s=s.replace('validateTask}from', 'validateTask,stepSchedule,reconcileSteps,taskEmoji}from')
s="import {enhanceSelect} from './select-ui.mjs';\n"+s
s=s.replace('detached=false, toastTimeout;', 'detached=false, toastTimeout, detailTaskId=null;')
s=s.replace("function options(selected,allText='No goal · general focus')", "function options(selected,allText='No goal')")
start=s.index('function render(){');end=s.index('function renderTimeline(){',start)
s=s[:start]+'''function render(){
  if(!state.goals.some(g=>g.id===state.selectedGoal))state.selectedGoal=state.goals[0]?.id||'';
  $('goalFilter').innerHTML=state.goals.length?state.goals.map(g=>`<option value="${esc(g.id)}" ${g.id===state.selectedGoal?'selected':''}>${esc(g.name)}</option>`).join(''):'<option value="" disabled selected>Choose a goal</option>';
  $('headerDate').textContent=niceDate(selectedDate,{weekday:'short',month:'short',day:'numeric'});
  $('todayButton').textContent=selectedDate===dayKey()?'Today':niceDate(selectedDate);
  renderTimeline();renderStats();renderFocus();
}
''' +s[end:]
s=s.replace('function renderTimeline(){const tasks=', "function renderTimeline(){if(detailTaskId&&state.tasks.some(t=>t.id===detailTaskId)){renderDetail();return;}detailTaskId=null;$('taskDetail').hidden=true;$('timelineScroll').hidden=false;$('addTask').hidden=false;document.querySelector('.schedule-footer').hidden=false;$('scheduleHeading').textContent='Your day';const tasks=")
s=s.replace('<span class="task-name">${esc(t.title)}</span>', '<span class="task-name">${esc(t.title)} <span class="task-emoji" aria-hidden="true">${taskEmoji(t.title,t.kind)}</span></span>')
start=s.index('if(!tasks.length)html+=');end=s.index('const mins=tasks.reduce',start)
s=s[:start]+'''$('timeline').innerHTML=html;
$('timelineScroll').classList.toggle('is-empty',!tasks.length);$('timelineScroll').inert=!tasks.length;
$('emptyDay').hidden=!!tasks.length;
$('emptyDay').innerHTML=!tasks.length?`<span class="empty-symbol" aria-hidden="true">✳</span><h3>A little room to begin.</h3><button class="primary" id="emptyAddTask">Add a task</button>${!state.tasks.length?'<button class="text-button" id="emptySample">Explore a sample day</button>':''}`:'';
$('timeline').querySelectorAll('[data-task]').forEach(b=>b.onclick=()=>{detailTaskId=b.dataset.task;renderTimeline();});
if($('emptyAddTask'))$('emptyAddTask').onclick=()=>openTask();if($('emptySample'))$('emptySample').onclick=loadSample;
''' +s[end:]
s=s.replace(":'A fresh start, at your pace'", ":''")
s=s.replace("const id=state.selectedGoal,p=progress(state.tasks,id),sessions=state.sessions.filter(s=>!id||s.goalId===id)","const id=state.selectedGoal,p=id?progress(state.tasks,id):{total:0,complete:0,percent:0},sessions=state.sessions.filter(s=>id&&s.goalId===id)")
s=s.replace("if(state.active&&(!id||state.active.goalId===id))", "if(state.active&&id&&state.active.goalId===id)")
s=s.replace("`${sessions.length} focus ${sessions.length===1?'session':'sessions'} logged`:'Your first session starts here'", "`${sessions.length} ${sessions.length===1?'session':'sessions'}`:'0 sessions'")
s=s.replace("`${p.complete} of ${p.total} planned steps completed`:'No steps planned yet'", "`${p.complete} of ${p.total} tasks completed`:'No tasks yet'")
s=s.replace("'Across all your goals'", "'Choose a goal'")
s=s.replace("s?s.title:'Start a new session'", "s?`${s.title} ${taskEmoji(s.title)}`:'Your next session'")
s=s.replace("s.step||(s.goalId?goalName(s.goalId):s.taskId?'Your scheduled task':'Independent focus')", "s.step||(s.taskId?'Scheduled task':'Independent session')")
s=s.replace(":'One thing at a time.'", ":''")
s=s.replace("'A LITTLE MOMENTUM':active.status==='ended'?'A MOMENT TO REFLECT':'TAKE YOUR TIME'", "'FOCUSING':active.status==='ended'?'FINISHED':'PAUSED'")
s=s.replace("'READY WHEN YOU ARE':'MINUTES OF POSSIBILITY'", "'READY':'MINUTES'")
s=s.replace("$('taskStep').value=task?.step||'';", "$('taskSteps').value=(task?stepsFor(task):[]).map(x=>x.title).join('\\n');$('substepsLabel').hidden=task?.kind==='commitment';")
s=s.replace("step:$('taskStep').value.trim(),", "step:'',substeps:[],")
s=s.replace("const error=validateTask(task,state.tasks);", "const titles=$('taskSteps').value.split('\\n').map(v=>v.trim()).filter(Boolean);if(task.kind==='task'&&titles.length>minuteOf(task.end)-minuteOf(task.start)){$('taskError').textContent='Allow at least one minute per substep.';return;}task.substeps=task.kind==='task'?reconcileSteps(prior?stepsFor(prior):[],titles,uid):[];task.step=task.substeps.find(v=>!v.done)?.title||'';const error=validateTask(task,state.tasks);")
s=s.replace("$('taskKind').onchange=()=>{", "$('taskKind').onchange=()=>{$('substepsLabel').hidden=$('taskKind').value==='commitment';")
s=s.replace("toast(prior?'Your schedule is updated.':'A little structure added to your day.')", "toast(prior?'Task updated.':'Task added.')")
s=s.replace("toast('Your goal has a place. Now add a small next step.')", "toast('Goal added.')")
s=s.replace("$('addGoal').onclick=$('goalsNav').onclick=openGoals;", "$('goalsNav').onclick=openGoals;")
s=s.replace("function moveDay(delta){", "function moveDay(delta){detailTaskId=null;")
s=s.replace("selectedDate=dayKey();render();", "selectedDate=dayKey();detailTaskId=null;render();")
s=s.replace("toast('Sample day loaded. All of this data is just for exploring.');", "toast(\"You're exploring a sample day.\");")
s=s.replace("$('sampleDay').onclick=loadSample;$('clearDemo').onclick=()=>{if(confirm('Remove the sample day and start fresh? Any changes made to the sample will be removed.'))reset();};", "$('sampleDay').onclick=loadSample;")
s=s.replace("state=emptyState();prepared=null;", "state=emptyState();detailTaskId=null;prepared=null;")
s=s.replace("$('quoteIntro').textContent=q[0];", "")
s=s.replace("const q=quotes[new Date().getDate()%quotes.length];", "document.querySelectorAll('select').forEach(select=>enhanceSelect(select,select.id==='goalFilter'?{footerLabel:'Manage goals',onFooter:openGoals}:{}));const q=quotes[new Date().getDate()%quotes.length];")
s=s.replace("if(storageError)toast", "if(state.demo)toast(\"You're exploring a sample day.\");if(storageError)toast")
# Sample task includes meaningful manually defined example substeps.
s=s.replace("state.sessions=[{id:uid(),date:today", "state.tasks.forEach(t=>{const titles=t.title==='Job search'?['Find three roles','Tailor my resume','Send applications']:t.title==='Explore portfolio ideas'?['Collect references','Sketch three directions','Choose a direction']:t.step?[t.step]:[];t.substeps=titles.map(title=>({id:uid(),title,done:t.done}));});state.sessions=[{id:uid(),date:today")
# Existing tasks migrate lazily without losing original next-step text.
insert=s.index('function renderStats(){')
s=s[:insert]+'''
function stepsFor(task){
  if(Array.isArray(task.substeps))return task.substeps;
  return task.step?[{id:task.id+'-first',title:task.step,done:!!task.done}]:[];
}
function minuteLabel(value){return `${String(Math.floor(value/60)).padStart(2,'0')}:${String(value%60).padStart(2,'0')}`;}
function renderDetail(){
  const task=state.tasks.find(t=>t.id===detailTaskId);if(!task){detailTaskId=null;renderTimeline();return;}
  $('timelineScroll').hidden=true;$('emptyDay').hidden=true;$('taskDetail').hidden=false;$('addTask').hidden=true;
  document.querySelector('.schedule-footer').hidden=true;$('scheduleHeading').textContent='Task breakdown';
  $('scheduleSummary').textContent=niceDate(task.date,{weekday:'short',month:'short',day:'numeric'});
  $('dayCaption').textContent=`${minuteOf(task.end)-minuteOf(task.start)} min`;
  const steps=stepSchedule({...task,substeps:stepsFor(task)}),count=steps.filter(s=>s.done).length;
  const totalMinutes=minuteOf(task.end)-minuteOf(task.start),pxPerMinute=Math.max(3,Math.min(10,420/totalMinutes));
  let rows='';
  for(const step of steps){
    const ticks=Array.from({length:step.minutes},(_,i)=>`<i class="minute-tick ${i%5===0?'major':''}" style="top:${i*pxPerMinute}px"></i>`).join('');
    rows+=`<div class="minute-step ${step.done?'completed':''}" style="min-height:${Math.max(step.minutes*pxPerMinute,80)}px"><div class="minute-scale"><time>${minuteLabel(step.startMinute)}</time>${ticks}</div><label class="substep-card"><input type="checkbox" data-step="${esc(step.id)}" ${step.done?'checked':''}><span><strong>${esc(step.title)}</strong><small>${step.minutes} min · ${minuteLabel(step.startMinute)}–${minuteLabel(step.endMinute)}</small></span></label></div>`;
  }
  $('taskDetail').innerHTML=`<div class="detail-toolbar"><button class="text-button" id="backToDay">${icon('left')}Back to day</button><button class="secondary small-button" id="editDetail">Edit task</button></div><div class="detail-heading"><h2>${esc(task.title)} <span aria-hidden="true">${taskEmoji(task.title,task.kind)}</span></h2><p>${fmtTime(task.start)} – ${fmtTime(task.end)}${task.goalId?' · '+esc(goalName(task.goalId)):''}</p></div>${steps.length?`<div class="detail-progress"><span>${count} of ${steps.length} substeps</span><div><i style="width:${count/steps.length*100}%"></i></div></div><div class="minute-timeline">${rows}<time class="end-time">${minuteLabel(minuteOf(task.end))}</time></div>`:`<div class="detail-empty"><p>${task.kind==='commitment'?'Time reserved.':'Break this task into smaller steps.'}</p>${task.kind==='task'?'<button class="secondary" id="addSubsteps">Add substeps</button>':''}</div>`}<div class="detail-actions">${task.kind==='task'?`<button class="primary" id="detailFocus" ${task.done?'disabled':''}>Focus on task</button><button class="secondary" id="detailComplete">${task.done?'Reopen task':'Mark complete'}</button>`:''}</div>`;
  $('backToDay').onclick=()=>{detailTaskId=null;renderTimeline();};$('editDetail').onclick=()=>openTask(task.id);
  if($('addSubsteps'))$('addSubsteps').onclick=()=>{openTask(task.id);$('taskSteps').focus();};
  $('taskDetail').querySelectorAll('[data-step]').forEach(input=>input.onchange=()=>{task.substeps=stepsFor(task).map(step=>step.id===input.dataset.step?{...step,done:input.checked}:step);task.step=task.substeps.find(step=>!step.done)?.title||'';if(!input.checked)task.done=false;if(prepared?.taskId===task.id)prepared.step=task.step;if(state.active?.taskId===task.id)state.active.step=task.step;snapshot();const scroll=$('taskDetail').scrollTop;renderDetail();$('taskDetail').scrollTop=scroll;renderFocus();renderStats();$('taskDetail').querySelector(`[data-step="${CSS.escape(input.dataset.step)}"]`)?.focus({preventScroll:true});});
  if($('detailFocus'))$('detailFocus').onclick=()=>{if(state.active){toast('Finish your current session first.');return;}prepared={taskId:task.id,goalId:task.goalId,title:task.title,step:task.step,remaining:initialSeconds(task),scheduled:true};detached=false;if(task.goalId){state.selectedGoal=task.goalId;save();render();}else renderFocus();document.querySelector('.focus-card').scrollIntoView({behavior:'smooth',block:'nearest'});};
  if($('detailComplete'))$('detailComplete').onclick=()=>{if(state.active?.taskId===task.id){endCheckIn();return;}task.done=!task.done;if(task.done)task.substeps=stepsFor(task).map(step=>({...step,done:true}));snapshot();renderDetail();renderStats();renderFocus();};
}
''' +s[insert:]
# Native label control no longer needs IDs that were removed.
p.write_text(s)
