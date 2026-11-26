export const dayKey=(date=new Date())=>`${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
export const minuteOf=time=>{const [h,m]=time.split(':').map(Number);return h*60+m;};
export const taskBounds=task=>({start:new Date(`${task.date}T${task.start}:00`).getTime(),end:new Date(`${task.date}T${task.end}:00`).getTime()});
export function currentTask(tasks,now=Date.now()){return tasks.filter(t=>t.kind==='task'&&!t.done).sort((a,b)=>a.start.localeCompare(b.start)).find(t=>{const b=taskBounds(t);return now>=b.start&&now<b.end;})||null;}
export function initialSeconds(task,now=Date.now()){const b=taskBounds(task);return Math.max(1,Math.round((b.end-(now>=b.start&&now<b.end?now:b.start))/1000));}
export function progress(tasks,goalId){const relevant=tasks.filter(t=>t.kind==='task'&&(!goalId||t.goalId===goalId));const complete=relevant.filter(t=>t.done).length;return{total:relevant.length,complete,percent:relevant.length?Math.round(complete/relevant.length*100):0};}
export function segmentSeconds(session,now=Date.now()){return session.runningSince?Math.max(0,(Math.min(now,session.endAt)-session.runningSince)/1000):0;}
export function remainingSeconds(session,now=Date.now()){return session.status==='running'?Math.max(0,Math.ceil((session.endAt-now)/1000)):Math.max(0,Math.ceil(session.remaining));}
export function validateTask(task,tasks){if(!task.title.trim())return 'Give your task a name.';if(!/^\d{4}-\d{2}-\d{2}$/.test(task.date)||!/^\d{2}:\d{2}$/.test(task.start)||!/^\d{2}:\d{2}$/.test(task.end)||!Number.isFinite(taskBounds(task).start))return 'Choose a valid date and time.';if(minuteOf(task.end)<=minuteOf(task.start))return 'The end time must be after the start time. Split overnight work into two tasks.';const conflict=tasks.find(t=>t.id!==task.id&&t.date===task.date&&minuteOf(task.start)<minuteOf(t.end)&&minuteOf(task.end)>minuteOf(t.start));return conflict?`This overlaps “${conflict.title}” (${conflict.start}–${conflict.end}). Choose another time.`:'';}

// Substeps are user-authored. Divide the scheduled block into whole-minute slices.
export function stepSchedule(task) {
  const steps = Array.isArray(task.substeps) ? task.substeps : [];
  const duration = minuteOf(task.end) - minuteOf(task.start);
  if (!steps.length || duration <= 0) return [];
  const base = Math.floor(duration / steps.length), remainder = duration % steps.length;
  let cursor = minuteOf(task.start);
  return steps.map((step, index) => {
    const minutes = base + (index < remainder ? 1 : 0);
    const result = {...step, startMinute: cursor, endMinute: cursor + minutes, minutes};
    cursor += minutes;
    return result;
  });
}
export function reconcileSteps(previous, titles, makeId) {
  const available = [...previous];
  return titles.map(title => {
    const index = available.findIndex(step => step.title === title);
    return index >= 0 ? available.splice(index, 1)[0] : {id: makeId(), title, done: false};
  });
}
export function taskEmoji(title, kind = 'task') {
  const rules = [[/job|application|career|resume|cv\b/i,'💼'],[/workout|gym|exercise|run\b|fitness|push day/i,'💪'],[/lunch|dinner|breakfast|meal|cook/i,'🍽️'],[/photo|camera|aperture/i,'📷'],[/read|book|study|learn|course|lesson/i,'📚'],[/design|sketch|portfolio|draw|art\b/i,'🎨'],[/code|develop|program|website/i,'💻'],[/write|draft|outline|journal/i,'✍️'],[/call|meeting|interview/i,'💬'],[/walk|outside|fresh air/i,'🌿'],[/idea|brainstorm|explore/i,'💡'],[/plan|priorit|day/i,'🗓️']];
  return rules.find(([pattern]) => pattern.test(title))?.[1] || (kind === 'commitment' ? '📅' : '🎯');
}
