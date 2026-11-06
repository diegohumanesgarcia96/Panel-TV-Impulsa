#!/usr/bin/env python3
"""Genera las versiones 'general' (sin hitos, para todas las sedes) a partir de
index.html (vertical Madrid) y horizontal.html (horizontal Madrid).
Uso: python3 build.py   → escribe general.html y general-horizontal.html"""
import re
# ---------- vertical general ----------
v=open('index.html').read()
v=v.replace('<div class="hitos"><h2>Próximos hitos</h2><div id="hitos"></div></div>\n','')
v=v.replace("document.getElementById('hitos').innerHTML=","var _h=document.getElementById('hitos'); if(_h) _h.innerHTML=")
v=v.replace('<meta name="claude:viewport-fit-sides" content="cover">','<meta name="claude:viewport-fit-sides" content="cover"><!-- versión general: sin hitos -->')
# sin hitos sobra altura: secciones proporcionales al nº de filas, filas repartidas y tipografía algo mayor
v=v.replace(".zones section { flex:1; display:flex; flex-direction:column; justify-content:center; }",
  ".zones section { display:flex; flex-direction:column; }\n.rows { flex:1; display:flex; flex-direction:column; justify-content:space-evenly; }\n.rows .pr { border-bottom:0; padding:0.2vmin 0; } .rows .pr + .pr { border-top:1px solid var(--line); }")
v=v.replace("'<section><h2>'+esc(z.zona)+'<span>'+tv+' viv. · '+ts+' vendidas</span></h2>'+rows+'</section>'",
  "'<section style=\"flex:'+(z.promos.length+1.3)+'\"><h2>'+esc(z.zona)+'<span>'+tv+' viv. · '+ts+' vendidas</span></h2><div class=\"rows\">'+rows+'</div></section>'")
v=v.replace("'<section><h2>Colombia<span>Hábitat Colombia · ventas sobre punto de equilibrio</span></h2>'+c+'</section>'",
  "'<section style=\"flex:'+(d.colombia.length+1.3)+'\"><h2>Colombia<span>Hábitat Colombia · ventas sobre punto de equilibrio</span></h2><div class=\"rows\">'+c+'</div></section>'")
assert v.count('class=\"rows\"')==2, v.count('rows')
for a,c in [(".pn { font-size: 1.68vmin;",".pn { font-size: 1.95vmin;"),(".pn .pl { display:block; font-size: 1.17vmin;",".pn .pl { display:block; font-size: 1.36vmin;"),
            (".pf { font-size: 1.24vmin;",".pf { font-size: 1.42vmin;"),(".pv { font-size: 1.68vmin;",".pv { font-size: 1.95vmin;"),(".pv span { color: var(--grey); font-weight: 500; font-size: 1.27vmin; }",".pv span { color: var(--grey); font-weight: 500; font-size: 1.45vmin; }"),
            ("section h2 { margin:0 0 0.33vmin; font-size: 1.92vmin;","section h2 { margin:0 0 0.5vmin; font-size: 2.2vmin;"),("section h2 span { color: var(--grey); text-transform:none; letter-spacing:0; font-weight:500; font-size: 1.45vmin; }","section h2 span { color: var(--grey); text-transform:none; letter-spacing:0; font-weight:500; font-size: 1.6vmin; }"),
            (".pb { height: 0.87vmin;",".pb { height: 1vmin;"),("grid-template-columns: 1fr 15.19vmin 19.17vmin 8.79vmin;","grid-template-columns: 1fr 16.5vmin 19.17vmin 9.5vmin;")]:
    assert a in v, a; v=v.replace(a,c)
assert 'id="hitos"' not in v
open('general.html','w').write(v)
# ---------- horizontal general: 3 columnas de zonas ----------
h=open('horizontal.html').read()
h=h.replace('<div class="main"><div class="col" id="colA"></div><div class="col" id="colB"></div>\n<div class="hitos"><h2>Próximos hitos</h2><div id="hitos"></div></div></div>',
            '<div class="main"><div class="col" id="colA"></div><div class="col" id="colB"></div><div class="col" id="colC"></div></div>')
h=h.replace("grid-template-columns: 1fr 1fr 0.55fr;","grid-template-columns: 1fr 1fr 1fr;")
# nombres a 2 líneas (columnas más estrechas, pero hay altura de sobra)
h=h.replace(".pn .pt { display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }",".pn .pt { display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }")
h=h.replace(".pn { font-size: 1.62vh;",".pn { font-size: 1.65vh;")
h=h.replace("grid-template-columns: 1fr 13.2vh 7vh 8.8vh;","grid-template-columns: 1fr 12.4vh 7vh 8vh;")
h=h.replace(".pf { font-size: 1.2vh;",".pf { font-size: 1.15vh;")
# reparto en 3 columnas (greedy por peso, orden de zonas)
old=re.search(r"  var tot=0; secs\.forEach.*?colB'\)\.innerHTML=b;", h, re.S).group(0)
new="""  var tot=0; secs.forEach(function(s){tot+=s.n;}); var cols=[[],[],[]], w=[0,0,0], k=0, acc=0;
  secs.forEach(function(s){ cols[k].push(s.h); w[k]+=s.n; acc+=s.n; if(k<2 && acc>=tot*(k+1)/3-0.5) k++; });
  document.getElementById('colA').innerHTML=cols[0].join(''); document.getElementById('colB').innerHTML=cols[1].join(''); document.getElementById('colC').innerHTML=cols[2].join('');"""
h=h.replace(old,new)
h=h.replace("document.getElementById('hitos').innerHTML=","var _h=document.getElementById('hitos'); if(_h) _h.innerHTML=")
assert 'id="hitos"' not in h and 'colC' in h
open('general-horizontal.html','w').write(h)
print("ok")
