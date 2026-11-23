#!/usr/bin/env python3
"""Genera las versiones 'general' (sin hitos, para todas las sedes) a partir de
index.html (vertical Madrid) y horizontal.html (horizontal Madrid).
Uso: python3 build.py   → escribe general.html y general-horizontal.html"""
import re
# ---------- vertical general ----------
v=open('index.html').read()
_o='<div class="bajo"><div class="hitos obj"><h2>Objetivos</h2><div id="objs"></div></div><div class="hitos"><h2>Agenda</h2><div id="hitos"></div></div></div>\n'; assert _o in v; v=v.replace(_o,'')
v=v.replace("document.getElementById('hitos').innerHTML=","var _h=document.getElementById('hitos'); if(_h) _h.innerHTML=")
v=v.replace('<meta name="claude:viewport-fit-sides" content="cover">','<meta name="claude:viewport-fit-sides" content="cover"><!-- versión general: sin hitos -->')
# sin hitos sobra altura: secciones proporcionales al nº de filas, filas repartidas y tipografía algo mayor
v=v.replace(".zones section { flex:1; display:flex; flex-direction:column; justify-content:center; }",
  ".zones section { display:flex; flex-direction:column; }\n.rows { flex:1; display:flex; flex-direction:column; justify-content:space-evenly; }\n.rows .pr { border-bottom:0; padding:0.2vmin 0; } .rows .pr + .pr { border-top:1px solid var(--line); }")
v=v.replace("'<section><h2><i class=\"zn\">'+esc(z.zona)+'</i>'+logoZ(z.zona)+'<span>'+fmtN(tv)+' viv. · '+fmtN(ts)+' vendidas</span></h2>'+rows+'</section>'",
  "'<section style=\"flex:'+(z.promos.length+1.3)+'\"><h2><i class=\"zn\">'+esc(z.zona)+'</i>'+logoZ(z.zona)+'<span>'+fmtN(tv)+' viv. · '+fmtN(ts)+' vendidas</span></h2><div class=\"rows\">'+rows+'</div></section>'")
v=v.replace("'<section><h2><i class=\"zn\">Colombia</i>'+logoZ('Colombia')+'<span>'+fmtN(ctv)+' viv. · '+fmtN(cts)+' vendidas</span></h2>'+c+'</section>'",
  "'<section style=\"flex:'+(d.colombia.length+1.3)+'\"><h2><i class=\"zn\">Colombia</i>'+logoZ('Colombia')+'<span>'+fmtN(ctv)+' viv. · '+fmtN(cts)+' vendidas</span></h2><div class=\"rows\">'+c+'</div></section>'")
assert v.count('class=\"rows\"')==2, v.count('rows')
for a,c in [(".pn { font-size: 1.68vmin;",".pn { font-size: 1.95vmin;"),(".pn .pl { display:block; font-size: 1.17vmin;",".pn .pl { display:block; font-size: 1.36vmin;"),
            (".pf { font-size: 1.24vmin;",".pf { font-size: 1.42vmin;"),(".pv { font-size: 1.68vmin;",".pv { font-size: 1.95vmin;"),(".pv span { color: var(--grey); font-weight: 500; font-size: 1.27vmin; }",".pv span { color: var(--grey); font-weight: 500; font-size: 1.45vmin; }"),
            ("section h2 { margin:0 0 0.33vmin; font-size: 1.92vmin;","section h2 { margin:0 0 0.5vmin; font-size: 2.2vmin;"),("section h2 span { color: var(--grey); text-transform:none; letter-spacing:0; font-weight:500; font-size: 1.45vmin; }","section h2 span { color: var(--grey); text-transform:none; letter-spacing:0; font-weight:500; font-size: 1.6vmin; }"),
            (".pb { height: 0.87vmin;",".pb { height: 1vmin;"),("grid-template-columns: 1fr 15.19vmin 19.17vmin 8.79vmin;","grid-template-columns: 1fr 16.5vmin 19.17vmin 9.5vmin;")]:
    assert a in v, a; v=v.replace(a,c)
assert 'id="hitos"' not in v and 'id="objs"' not in v
_r="OTRA='horizontal.html'"; assert _r in v; v=v.replace(_r,"OTRA='general-horizontal.html'")
open('general.html','w').write(v)
# ---------- horizontal general: 3 columnas de zonas ----------
h=open('horizontal.html').read()
h=h.replace('<div class="main"><div class="col" id="colA"></div><div class="col" id="colB"></div>\n<div class="lat"><div class="hitos obj"><h2>Objetivos</h2><div id="objs"></div></div><div class="hitos"><h2>Agenda</h2><div id="hitos"></div></div></div></div>',
            '<div class="main"><div class="col" id="colA"></div><div class="col" id="colB"></div><div class="col" id="colC"></div></div>')
h=h.replace("grid-template-columns: 1fr 1fr 0.55fr;","grid-template-columns: 1fr 1fr 1fr;")
# nombres a 2 líneas (columnas más estrechas, pero hay altura de sobra)
h=h.replace(".pn .pt { display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }",".pn .pt { display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }")
h=h.replace(".pn { font-size: calc(1.62 * var(--u));",".pn { font-size: calc(1.65 * var(--u));")
h=h.replace("grid-template-columns: 1fr calc(13.2 * var(--u)) calc(7 * var(--u)) calc(8.8 * var(--u));","grid-template-columns: 1fr calc(12.4 * var(--u)) calc(7 * var(--u)) calc(8 * var(--u));")
h=h.replace(".pf { font-size: calc(1.2 * var(--u));",".pf { font-size: calc(1.15 * var(--u));")
# reparto en 3 columnas (greedy por peso, orden de zonas)
old=re.search(r"  var tot=0; secs\.forEach.*?colB'\)\.innerHTML=b;", h, re.S).group(0)
new="""  var tot=0; secs.forEach(function(s){tot+=s.n;}); var cols=[[],[],[]], w=[0,0,0], k=0, acc=0;
  secs.forEach(function(s){ cols[k].push(s.h); w[k]+=s.n; acc+=s.n; if(k<2 && acc>=tot*(k+1)/3-0.5) k++; });
  document.getElementById('colA').innerHTML=cols[0].join(''); document.getElementById('colB').innerHTML=cols[1].join(''); document.getElementById('colC').innerHTML=cols[2].join('');"""
h=h.replace(old,new)
h=h.replace("document.getElementById('hitos').innerHTML=","var _h=document.getElementById('hitos'); if(_h) _h.innerHTML=")
assert 'id="hitos"' not in h and 'id="objs"' not in h and 'colC' in h
# 20/11/2026: con nombres a 2 líneas el recorte de letras se evita con más interlínea (no con relleno, que dejaría ver la 3ª línea)
_a=".pn .pt { padding-bottom:0.22em; margin-bottom:-0.22em; padding-top:0.2em; margin-top:-0.2em; }"
assert _a in h; h=h.replace(_a,".pn .pt { line-height:1.4; padding-top:0.1em; margin-top:-0.22em; padding-bottom:0.1em; margin-bottom:-0.04em; }")
_r="OTRA='index.html'"; assert _r in h; h=h.replace(_r,"OTRA='general.html'")
import re as _re
_m=_re.search(r'/\*ENT-H\*/.*?/\*ENT-H-FIN\*/\n', h, _re.S); assert _m, 'bloque ENT-H'
h=h[:_m.start()]+'/* horizontal general: columnas estrechas, la entrega va en una línea propia bajo la localidad */\n.pn { display:block; } .pe { display:none; } .pnt { overflow:visible; }\n.pem { display:block; margin-top:0.3em; white-space:nowrap; } .pem i { display:none; }\n'+h[_m.end():]
open('general-horizontal.html','w').write(h)
print("ok")
