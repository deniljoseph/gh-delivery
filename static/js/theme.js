/* Theme handling shared by the office app, driver portal and login pages.
   accent theme -> <html data-theme>, light/dark -> <html data-bs-theme>; both remembered per device. */
(function(){
  var THEMES=[
    {id:'classic',name:'Classic',c:['#1a1a1a','#000000','#f4f4f4']},
    {id:'ocean',name:'Ocean',c:['#0b2545','#1565c0','#eef3f9']},
    {id:'forest',name:'Forest',c:['#12372a','#2e7d32','#eff5ef']},
    {id:'royal',name:'Royal',c:['#2a1b4d','#6a3fc4','#f3f0fa']},
    {id:'sunset',name:'Sunset',c:['#4a2310','#e65100','#fbf3ed']},
    {id:'crimson',name:'Crimson',c:['#4a0f1a','#c62828','#faf0f0']},
    {id:'teal',name:'Teal',c:['#0c3b3f','#00838f','#edf6f7']},
    {id:'gold',name:'Gold',c:['#2b2412','#a67608','#f8f5ec']},
    {id:'slate',name:'Slate',c:['#263238','#455a64','#f1f3f4']}
  ];
  var root=document.documentElement;
  function get(k,d){try{return localStorage.getItem(k)||d;}catch(e){return d;}}
  function put(k,v){try{localStorage.setItem(k,v);}catch(e){}}
  function valid(id){return THEMES.some(function(t){return t.id===id;});}
  function apply(){
    var a=get('ghaccent','classic'); if(!valid(a)) a='classic';
    root.setAttribute('data-theme',a);
    var sysDark=!!(window.GH_SYSTEM_DARK&&window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches);
    root.setAttribute('data-bs-theme',get('ghtheme',sysDark?'dark':'light')==='dark'?'dark':'light');
    var meta=document.querySelector('meta[name=theme-color]');
    if(meta){var side=getComputedStyle(root).getPropertyValue('--side').trim(); if(side) meta.setAttribute('content',side);}
    var di=document.getElementById('di'); if(di) di.className=root.getAttribute('data-bs-theme')==='dark'?'bi bi-sun':'bi bi-moon-stars';
    document.querySelectorAll('.theme-chip').forEach(function(c){c.classList.toggle('on',c.dataset.theme===a);});
  }
  window.ghTheme={
    setAccent:function(id){if(!valid(id)) return; put('ghaccent',id); apply();},
    toggleDark:function(){put('ghtheme',root.getAttribute('data-bs-theme')==='dark'?'light':'dark'); apply();},
    build:function(el){
      if(!el) return; el.innerHTML='';
      THEMES.forEach(function(t){
        var b=document.createElement('button'); b.type='button'; b.className='theme-chip'; b.dataset.theme=t.id;
        b.innerHTML='<div class="sw"><span style="background:'+t.c[0]+'"></span><span style="background:'+t.c[1]+'"></span><span style="background:'+t.c[2]+'"></span></div>'+t.name;
        b.onclick=function(){ghTheme.setAccent(t.id);}; el.appendChild(b);
      });
      var dm=document.createElement('button'); dm.type='button'; dm.className='theme-chip'; dm.style.gridColumn='1 / -1';
      dm.innerHTML='<i class="bi bi-circle-half me-1"></i>Switch light / dark'; dm.onclick=function(){ghTheme.toggleDark();}; el.appendChild(dm);
      apply();
    },
    apply:apply
  };
  apply();                                   // before first paint (script is loaded in <head>)
  document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('.theme-grid').forEach(ghTheme.build);apply();});
})();
