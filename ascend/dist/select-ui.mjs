// Native values remain the source of truth; the menu opens below its trigger.
export function enhanceSelect(select, {footerLabel, onFooter} = {}) {
  const label = select.getAttribute('aria-label') || select.closest('label')?.childNodes[0]?.textContent.trim() || 'Choose an option';
  const shell = document.createElement('div'); shell.className = 'select-shell';
  select.before(shell); shell.append(select); select.hidden = true; select.tabIndex = -1;
  const trigger = document.createElement('button'); trigger.type = 'button'; trigger.className = 'select-trigger';
  trigger.setAttribute('aria-label', label); trigger.setAttribute('aria-haspopup', 'listbox'); trigger.setAttribute('aria-expanded', 'false');
  const value = document.createElement('span'); trigger.append(value);
  const chevron = document.createElement('span'); chevron.className = 'select-chevron'; chevron.setAttribute('aria-hidden','true'); trigger.append(chevron);
  const menu = document.createElement('div'); menu.id = select.id + '-menu'; menu.className = 'select-menu'; menu.setAttribute('popover','auto'); menu.setAttribute('role','listbox'); menu.setAttribute('aria-label',label);
  trigger.setAttribute('aria-controls',menu.id); shell.append(trigger,menu);
  function sync() {
    value.textContent = select.selectedOptions[0]?.textContent || 'Choose a goal'; trigger.disabled = select.disabled;
    menu.replaceChildren();
    [...select.options].forEach(option => {
      const item = document.createElement('button'); item.type = 'button'; item.className = 'select-option'; item.textContent = option.textContent;
      item.setAttribute('role','option'); item.setAttribute('aria-selected',String(option.selected)); item.disabled = option.disabled;
      item.onclick = () => {select.value=option.value; menu.hidePopover(); select.dispatchEvent(new Event('change',{bubbles:true})); sync(); trigger.focus();};
      menu.append(item);
    });
    if (footerLabel) {const footer=document.createElement('button');footer.type='button';footer.className='select-footer';footer.textContent=footerLabel;footer.onclick=()=>{menu.hidePopover();onFooter();};menu.append(footer);}
  }
  function open() {
    const rect = trigger.getBoundingClientRect();
    menu.style.left = `${Math.max(8,Math.min(rect.left,innerWidth-Math.max(rect.width,170)-8))}px`;
    menu.style.top = `${rect.bottom+7}px`; menu.style.width = `${Math.max(rect.width,170)}px`;
    menu.style.maxHeight = `${Math.max(75,Math.min(270,innerHeight-rect.bottom-15))}px`;
    menu.showPopover(); menu.querySelector('[aria-selected="true"]:not(:disabled),button:not(:disabled)')?.focus();
  }
  trigger.onclick=()=>menu.matches(':popover-open')?menu.hidePopover():open();
  trigger.onkeydown=e=>{if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();open();}};
  menu.onkeydown=e=>{
    const items=[...menu.querySelectorAll('button:not(:disabled)')], index=items.indexOf(document.activeElement);
    if(['ArrowDown','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?items.length-1:(index+(e.key==='ArrowDown'?1:-1)+items.length)%items.length;items[next]?.focus();}
    if(e.key==='Escape'){e.preventDefault();menu.hidePopover();trigger.focus();}
    if(e.key==='Tab')menu.hidePopover();
  };
  menu.addEventListener('toggle',()=>{const open=menu.matches(':popover-open');trigger.setAttribute('aria-expanded',String(open));shell.classList.toggle('open',open);});
  select.addEventListener('change',sync);
  new MutationObserver(sync).observe(select,{childList:true,subtree:true,attributes:true,attributeFilter:['disabled','selected']});
  select.form?.addEventListener('reset',()=>queueMicrotask(sync));
  window.addEventListener('resize',()=>{if(menu.matches(':popover-open'))menu.hidePopover();});
  sync(); return {sync};
}
