(function(){
  var im=document.querySelector('.hero-bg');if(!im)return;function go(){requestAnimationFrame(function(){im.classList.add('in');});}
  if(im.complete&&im.naturalWidth>0)go();else im.addEventListener('load',go);
})();
(function(){
  var t=document.getElementById('logoTrack');if(!t)return;var base=[].slice.call(t.children),timer;
  function build(){
    t.classList.remove('ready');
    while(t.children.length>base.length)t.removeChild(t.lastChild);
    var gap=parseFloat(getComputedStyle(t).gap)||64,w=base.reduce(function(a,i){return a+i.getBoundingClientRect().width;},0)+gap*base.length;
    var copies=Math.max(2,Math.ceil((innerWidth*2)/w)+1);
    for(var c=1;c<copies;c++)base.forEach(function(i){var k=i.cloneNode(true);k.setAttribute('alt','');k.setAttribute('aria-hidden','true');t.appendChild(k);});
    t.style.setProperty('--shift',w+'px');t.style.setProperty('--dur',Math.round(w/38)+'s');
    void t.offsetWidth;t.classList.add('ready');
  }
  if(document.readyState==='complete')build();else addEventListener('load',build);
  addEventListener('resize',function(){clearTimeout(timer);timer=setTimeout(build,200);});
})();
(function(){
  var h=document.querySelector('header');if(!h)return;if(!document.querySelector('.hero,.art-hero')){h.classList.add('scrolled');return;}function onS(){h.classList.toggle('scrolled',scrollY>40);}addEventListener('scroll',onS,{passive:true});onS();
})();
(function(){
  var burger=document.querySelector('header .burger'),menu=document.querySelector('header .menu'),head=document.querySelector('header');
  if(!burger||!menu||!head)return;
  var panel=document.createElement('nav');
  panel.className='mobile-nav';panel.id='mobileNav';panel.setAttribute('aria-label','Menu principal');panel.hidden=true;
  var list=document.createElement('ul');
  [].forEach.call(menu.querySelectorAll('a'),function(a){
    var li=document.createElement('li');li.appendChild(a.cloneNode(true));list.appendChild(li);
  });
  panel.appendChild(list);
  var cta=document.querySelector('header .nav-actions .btn');
  if(cta){var c=cta.cloneNode(true);c.className='btn btn-dark mobile-cta';panel.appendChild(c);}
  head.appendChild(panel);
  var scrim=document.createElement('div');scrim.className='nav-scrim';scrim.hidden=true;
  document.body.appendChild(scrim);
  burger.setAttribute('aria-expanded','false');burger.setAttribute('aria-controls','mobileNav');
  function set(open){
    burger.setAttribute('aria-expanded',String(open));
    burger.classList.toggle('open',open);
    panel.hidden=!open;scrim.hidden=!open;
    head.classList.toggle('nav-open',open);
    document.documentElement.classList.toggle('nav-open',open);
  }
  burger.addEventListener('click',function(){set(burger.getAttribute('aria-expanded')!=='true');});
  scrim.addEventListener('click',function(){set(false);});
  panel.addEventListener('click',function(e){if(e.target.closest('a'))set(false);});
  addEventListener('keydown',function(e){if(e.key==='Escape')set(false);});
  addEventListener('resize',function(){if(innerWidth>900)set(false);});
})();
