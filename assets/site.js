(function(){
  // Ferme le menu déroulant quand on clique ailleurs
  document.addEventListener('click',function(e){
    document.querySelectorAll('details.dd[open],details.menu-btn[open]').forEach(function(d){ if(!d.contains(e.target)) d.removeAttribute('open'); });
  });

  // Pré-sélection du service depuis l'ancre (contact.html#bornage)
  var sel=document.getElementById('f-service');
  if(sel && location.hash){
    var h=location.hash.slice(1);
    Array.prototype.forEach.call(sel.options,function(o){ if(o.dataset.key===h) sel.value=o.value; });
  }

  // Formulaire de devis
  var form=document.getElementById('devis-form');
  if(!form) return;
  form.addEventListener('submit',function(e){
    e.preventDefault();
    if(!form.reportValidity()) return;
    var v=function(id){var el=document.getElementById(id);return el?el.value.trim():'';};
    var body=[
      'Demande de devis — site gemetric.fr','',
      'Nom : '+v('f-nom'),
      'E-mail : '+v('f-email'),
      'Téléphone : '+v('f-tel'),
      'Vous êtes intéressé pour : '+v('f-service'),
      'Adresse du bien : '+v('f-adresse'),
      'Échéance : '+v('f-delai'),'',
      'Message :',v('f-message')
    ].join('\n');
    var done=document.getElementById('devis-done');
    document.getElementById('devis-text').textContent=body;
    var mail=document.getElementById('devis-mailto');
    mail.href='mailto:contact@gemetric.fr?subject='+encodeURIComponent('Demande de devis — '+v('f-service'))+'&body='+encodeURIComponent(body);
    form.hidden=true; done.hidden=false;
    // Point d'accroche analytics : window.dataLayer
    try{(window.dataLayer=window.dataLayer||[]).push({event:'generate_lead',service:v('f-service')});}catch(err){}
    done.scrollIntoView({behavior:'smooth',block:'start'});
  });
  var copy=document.getElementById('devis-copy');
  if(copy) copy.addEventListener('click',function(){
    var pre=document.getElementById('devis-text');
    var ok=function(){copy.textContent='Copié';setTimeout(function(){copy.textContent='Copier la demande';},2000);};
    var fallback=function(){var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);copy.textContent='Texte sélectionné';};
    try{navigator.clipboard.writeText(pre.textContent).then(ok,fallback);}catch(err){fallback();}
  });
  var edit=document.getElementById('devis-edit');
  if(edit) edit.addEventListener('click',function(){form.hidden=false;document.getElementById('devis-done').hidden=true;});
})();

/* ===== Motion : révélations, compteurs, en-tête, parallaxe ===== */
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  if (reduce) { document.querySelectorAll('svg').forEach(function(sv){ if (sv.pauseAnimations) { try { sv.setCurrentTime(8); sv.pauseAnimations(); } catch(e){} } }); }
  if (!('IntersectionObserver' in window) || reduce) return;
  root.classList.add('js');
  // Révélations : les éléments déjà visibles au chargement sont marqués tout de suite
  var targets = document.querySelectorAll('.rv, .rv-group, .photo, .hero-home, .hero-city');
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
  }, {rootMargin:'0px 0px -8% 0px', threshold:0.08});
  targets.forEach(function(el){
    var r = el.getBoundingClientRect();
    if (r.top < innerHeight * 0.92) { requestAnimationFrame(function(){ el.classList.add('in'); }); }
    else io.observe(el);
  });
  // Filet de sécurité : tout est révélé au bout de 4 s quoi qu'il arrive
  setTimeout(function(){ targets.forEach(function(el){ el.classList.add('in'); }); }, 4000);

  // Compteurs (la valeur finale est dans le HTML)
  var cio = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting) return; cio.unobserve(e.target);
      var el = e.target, end = parseInt(el.dataset.count,10), t0 = null, dur = 1400;
      function step(t){ if(!t0) t0=t; var k=Math.min(1,(t-t0)/dur); el.textContent = Math.round(end*(1-Math.pow(1-k,3))); if(k<1) requestAnimationFrame(step); }
      requestAnimationFrame(step);
    });
  }, {threshold:0.6});
  document.querySelectorAll('[data-count]').forEach(function(el){ cio.observe(el); });

  // En-tête compact au scroll + parallaxe légère des fonds photo
  var bgs = document.querySelectorAll('.stats-bg');
  var ticking = false;
  function onScroll(){
    root.classList.toggle('is-scrolled', scrollY > 30);
    bgs.forEach(function(img){
      var r = img.parentNode.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      var p = (r.top + r.height/2 - innerHeight/2) / innerHeight;
      img.style.transform = 'scale(1.12) translateY(' + (p * -40).toFixed(1) + 'px)';
    });
    ticking = false;
  }
  addEventListener('scroll', function(){ if(!ticking){ ticking = true; requestAnimationFrame(onScroll); } }, {passive:true});
  onScroll();
})();
