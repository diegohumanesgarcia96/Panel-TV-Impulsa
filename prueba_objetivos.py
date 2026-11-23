# PRUEBA (23/11/2026, petición de Miguel Ángel): en los paneles de Madrid, Objetivos del acta de coordinadores a la izquierda
# y Próximos hitos a la derecha, sin repetir: los hitos marcados "objetivo": true en datos.json no salen en hitos (su fecha va en el objetivo).
JS = r"""
function renderObjs(d){ var el=document.getElementById('objs'); if(!el) return false; var L=(d.objetivos&&d.objetivos.lista)||[]; if(!L.length){ el.parentNode.style.display='none'; return false; }
  var MM=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
  el.innerHTML=L.map(function(o){ var f=''; if(o.fecha){ var a=String(o.fecha).split('-'); f=a.length>2?(+a[2])+' '+MM[+a[1]-1]:MM[+a[1]-1]+' '+a[0]; }
    return '<div class="ob"><div><b>'+esc(o.ambito)+'</b><span>'+esc(o.texto)+'</span></div>'+(f?'<em>'+f+'</em>':'')+'</div>'; }).join('');
  return true; }
function renderHitos(d){
  var conObjs=renderObjs(d);
"""
def patch(f, html_old, html_new, css, lim):
    s=open(f).read(); assert 'renderObjs' not in s
    assert s.count(html_old)==1,f; s=s.replace(html_old,html_new)
    a="function renderHitos(d){\n"; assert s.count(a)==1; s=s.replace(a,JS.lstrip('\n'))
    b="else prox.push({x:x,f:f,dias:dias}); });"; assert s.count(b)==1
    s=s.replace(b,"else if(!(conObjs&&x.objetivo)) prox.push({x:x,f:f,dias:dias}); });")
    c="prox=prox.slice(0,6);"; assert s.count(c)==1; s=s.replace(c,"prox=prox.slice(0,conObjs?%d:6);"%lim)
    k=s.rindex('</style>'); s=s[:k]+css+s[k:]; open(f,'w').write(s)
CSS_V = """
/* PRUEBA objetivos + hitos (vertical Madrid) */
.bajo { display:grid; grid-template-columns: 1fr 1fr; gap: 1.1vmin; align-items:stretch; }
.bajo .hitos { display:flex; flex-direction:column; min-width:0; }
#objs, .bajo #hitos { flex:1; display:flex; flex-direction:column; justify-content:space-evenly; }
.ob { display:grid; grid-template-columns: 1fr auto; gap: 1.12vmin; align-items:center; padding: 0.24vmin 0; border-bottom:1px solid var(--line); }
.ob:last-child { border-bottom:0; }
.ob b { display:block; font-size: 1.52vmin; font-weight:600; line-height:1.2; }
.ob span { display:block; font-size: 1.24vmin; color: var(--grey); line-height:1.25; text-wrap:balance; }
.ob em { font-style:normal; font-size: 1.24vmin; font-weight:600; color: var(--car); white-space:nowrap; }
@media (max-width: 700px) { .bajo { grid-template-columns: 1fr; } .ob b { font-size: 2.72vmin; } .ob span, .ob em { font-size: 1.92vmin; } }
"""
CSS_H = """
/* PRUEBA objetivos + hitos (horizontal Madrid): la columna derecha se reparte entre los dos bloques */
.lat { display:flex; flex-direction:column; gap: calc(1.4 * var(--u)); min-height:0; }
.lat .hitos { flex:1 1 0; } .lat .hitos.obj { flex:0 0 auto; }
#objs { display:flex; flex-direction:column; }
.ob { display:grid; grid-template-columns: 1fr auto; gap: calc(1 * var(--u)); align-items:center; padding: calc(0.55 * var(--u)) 0; border-bottom:1px solid var(--line); }
.ob:last-child { border-bottom:0; }
.ob b { display:block; font-size: calc(1.62 * var(--u)); font-weight:600; line-height:1.2; }
.ob span { display:block; font-size: calc(1.35 * var(--u)); color: var(--grey); line-height:1.25; text-wrap:balance; }
.ob em { font-style:normal; font-size: calc(1.35 * var(--u)); font-weight:600; color: var(--car); white-space:nowrap; }
.lat.cmp .ob { padding: calc(0.3 * var(--u)) 0; } .lat.cmp .hi { padding: calc(0.25 * var(--u)) 0; } .lat.cmp .hitos h2 { margin-bottom: calc(0.2 * var(--u)); } .lat.cmp .hitos { padding-top: calc(0.7 * var(--u)); padding-bottom: calc(0.7 * var(--u)); } .lat.cmp .ht span { display:none; }
.lat #hitos { overflow:hidden; } .lat .ht { font-size: calc(1.62 * var(--u)); } .lat .hd { font-size: calc(1.9 * var(--u)); } .lat .hi { grid-template-columns: calc(8.6 * var(--u)) 1fr; padding: calc(0.5 * var(--u)) 0; }
"""
patch('prueba.html','<div class="hitos"><h2>Próximos hitos</h2><div id="hitos"></div></div>',
      '<div class="bajo"><div class="hitos obj"><h2>Objetivos semanales</h2><div id="objs"></div></div><div class="hitos"><h2>Próximos hitos</h2><div id="hitos"></div></div></div>', CSS_V, 6)
patch('prueba-horizontal.html','<div class="hitos"><h2>Próximos hitos</h2><div id="hitos"></div></div>',
      '<div class="lat"><div class="hitos obj"><h2>Objetivos semanales</h2><div id="objs"></div></div><div class="hitos"><h2>Próximos hitos</h2><div id="hitos"></div></div></div>', CSS_H, 5)
# horizontal: si los hitos no caben en su bloque, se quitan los más lejanos
s=open('prueba-horizontal.html').read()
a="  document.getElementById('hitos').innerHTML=out||'<div class=\"hi\"><div class=\"ht\">Sin hitos próximos</div></div>';\n}"
assert s.count(a)==1
s=s.replace(a,a[:-1]+"  ajustaLat(); if(document.fonts&&document.fonts.ready) document.fonts.ready.then(ajustaLat);\n}\nfunction ajustaLat(){ var h=document.getElementById('hitos'); if(!h||!document.getElementById('objs')) return; var hs=h.querySelectorAll('.hi'), i=hs.length-1; while(i>=4 && h.scrollHeight>h.clientHeight+1){ hs[i].parentNode.removeChild(hs[i]); i--; } if(h.scrollHeight>h.clientHeight+1){ h.parentNode.parentNode.className+=' cmp'; } }")
open('prueba-horizontal.html','w').write(s)
v=open('prueba.html').read(); x="while(i>=3 && document.documentElement.scrollHeight"; assert v.count(x)==1; open('prueba.html','w').write(v.replace(x,"while(i>=4 && document.documentElement.scrollHeight"))
print('objetivos montados en prueba')
