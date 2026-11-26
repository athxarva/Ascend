import test from 'node:test';
import assert from 'node:assert/strict';
import{currentTask,initialSeconds,progress,remainingSeconds,segmentSeconds,validateTask}from'../dist/core.mjs';
const task={id:'t',title:'Write outline',kind:'task',goalId:'g',date:'2026-11-25',start:'10:00',end:'11:00',done:false};
const at=time=>new Date(`2026-11-25T${time}:00`).getTime();
test('current scheduled task follows local time, excludes commitments and completed tasks',()=>{assert.equal(currentTask([task],at('10:00')).id,'t');assert.equal(currentTask([task],at('11:00')),null);assert.equal(currentTask([{...task,done:true}],at('10:30')),null);assert.equal(currentTask([{...task,kind:'commitment'}],at('10:30')),null);});
test('late start uses remaining slot; future task uses its full duration',()=>{assert.equal(initialSeconds(task,at('10:20')),2400);assert.equal(initialSeconds(task,at('09:00')),3600);});
test('goal completion excludes commitments and changes with added tasks',()=>{const tasks=[{...task,done:true},{...task,id:'b'},{...task,id:'c',kind:'commitment',done:true},{...task,id:'d',goalId:'other',done:true}];assert.deepEqual(progress(tasks,'g'),{total:2,complete:1,percent:50});assert.equal(progress([...tasks,{...task,id:'new'}],'g').percent,33);assert.equal(progress([],'g').percent,0);});
test('elapsed time uses clock and stops at deadline after background throttling',()=>{const s={status:'running',runningSince:1000,endAt:61000,remaining:60};assert.equal(remainingSeconds(s,31000),30);assert.equal(segmentSeconds(s,31000),30);assert.equal(segmentSeconds(s,90000),60);assert.equal(remainingSeconds(s,90000),0);assert.equal(remainingSeconds({...s,status:'paused',remaining:28},90000),28);});
test('overlaps are blocked, adjacent tasks and editing same task are allowed',()=>{assert.match(validateTask({...task,id:'b',start:'10:30',end:'11:30'},[task]),/overlaps/);assert.equal(validateTask({...task,id:'b',start:'11:00',end:'12:00'},[task]),'');assert.equal(validateTask(task,[task]),'');assert.match(validateTask({...task,end:'09:00'},[]),/end time/);});

import {stepSchedule,reconcileSteps,taskEmoji} from '../dist/core.mjs';
test('substeps exactly cover a block in whole minutes, including remainders',()=>{
  const steps=[{id:'a',title:'Find roles'},{id:'b',title:'Tailor resume'},{id:'c',title:'Apply'}];
  const slices=stepSchedule({...task,end:'10:50',substeps:steps});
  assert.deepEqual(slices.map(s=>s.minutes),[17,17,16]);
  assert.equal(slices[0].startMinute,600);
  assert.equal(slices[2].endMinute,650);
  assert.equal(slices[1].startMinute,slices[0].endMinute);
  assert.deepEqual(stepSchedule(task),[]);
});
test('editing and reordering substeps preserves checked state without duplicate IDs',()=>{
  let next=0;const previous=[{id:'a',title:'Read',done:true},{id:'b',title:'Write',done:false}];
  const result=reconcileSteps(previous,['Write','Read','Read'],()=>`new-${++next}`);
  assert.equal(result[0].id,'b');assert.equal(result[1].done,true);assert.equal(result[2].done,false);
  assert.equal(new Set(result.map(s=>s.id)).size,3);
});
test('task emoji reflects common task categories with a stable fallback',()=>{
  assert.equal(taskEmoji('Job search'),'💼');assert.equal(taskEmoji('Read about aperture'),'📷');
  assert.equal(taskEmoji('Something personal'),'🎯');assert.equal(taskEmoji('Appointment','commitment'),'📅');
});
