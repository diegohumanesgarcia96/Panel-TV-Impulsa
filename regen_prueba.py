# Regenera las páginas de prueba a partir de las definitivas: mismas páginas + fila de terceros de Sevilla (pendiente de datos de Alfonso)
FT="function filaT(t){ return '<div class=\"pr\"><div class=\"pn\"><div class=\"pnt\"><span class=\"pt\">'+nomb(t.nombre)+'</span><span class=\"pl\">'+esc(t.localidad)+'</span></div></div><div class=\"pf\">'+esc(t.fase||'Comercialización')+'</div><div></div><div class=\"pv\">'+fmtN(t.viviendas)+'<span>\\u00a0viv.</span></div></div>'; }\nfunction render(d){"
M={'index.html':('prueba.html',"OTRA='horizontal.html'","OTRA='prueba-horizontal.html'"),'horizontal.html':('prueba-horizontal.html',"OTRA='index.html'","OTRA='prueba.html'"),'general.html':('prueba-general.html',"OTRA='general-horizontal.html'","OTRA='prueba-general-horizontal.html'"),'general-horizontal.html':('prueba-general-horizontal.html',"OTRA='general.html'","OTRA='prueba-general.html'")}
for r,(p,a,b) in M.items():
    s=open(r).read(); assert a in s; s=s.replace(a,b)
    if r!='index.html':
        assert s.count('function render(d){')==1; s=s.replace('function render(d){',FT)
        if 'horizontal' in r:
            x="p.viviendas>0&&p.vendidas>=p.viviendas,p.maps,entrega(p)); });\n"; assert s.count(x)==1,r
            s=s.replace(x,x+"    var nt=0; if(z.terceros){ rows+=filaT(z.terceros); nt=1; }\n")
            assert s.count('z.promos.length+1.2')==2; s=s.replace('z.promos.length+1.2','z.promos.length+nt+1.2')
        else:
            x="    h+='<section style=\"flex:'+(z.promos.length+1.3)+'\">"; assert s.count(x)==1
            s=s.replace(x,"    var nt=0; if(z.terceros){ rows+=filaT(z.terceros); nt=1; }\n    h+='<section style=\"flex:'+(z.promos.length+nt+1.3)+'\">")
    # PRUEBA 23/11 (Miguel): cifras DENTRO de la barra, sin número a la derecha.
    # Por defecto: vendidas (izq.) y TOTAL (dcha.). Con ?quedan en la dirección: vendidas y las que QUEDAN.
    # Cada cifra va entera de un solo color: blanca si el naranja la cubre, oscura si no (ajustaBarras la recoloca si el borde la cortaría).
    hz='horizontal' in r; gen='general' in r
    x="<div class=\"pb\"><i style=\"width:'+Math.max(0,Math.min(100,Math.round(pct)))+'%\"></i></div><div class=\"pv\">'+s+'<span>/'+v+'</span></div></div>'"
    assert s.count(x)==1,r; s=s.replace(x,"'+barra(pct,s,v)+'</div>'")
    BJ=r"""var QUEDAN=/[?&]quedan/.test(location.search);
function barra(pct,s,v){ var ns=+String(s).replace(/\./g,''), nv=+String(v).replace(/\./g,''), q=Math.max(0,nv-ns), p=nv>0?Math.max(0,Math.min(100,ns/nv*100)):0, d=QUEDAN?(q>0?fmtN(q):''):fmtN(nv);
  return '<div class="pb2" data-p="'+p+'" title="'+fmtN(ns)+' vendidas de '+fmtN(nv)+' · '+fmtN(q)+' disponibles"><i style="width:'+p+'%"></i><b class="a">'+fmtN(ns)+'</b><b class="q">'+d+'</b></div>'; }
function ajustaBarras(){ var L=document.querySelectorAll('.pb2'); for(var k=0;k<L.length;k++){ var x=L[k], W=x.clientWidth; if(!W) continue; var a=x.querySelector('.a'), q=x.querySelector('.q'); a.style.left=''; q.style.right=''; a.className='a'; q.className='q';
    var pad=parseFloat(getComputedStyle(a).left)||0, f=W*(+x.getAttribute('data-p'))/100, wa=a.offsetWidth, wq=q.textContent?q.offsetWidth:0;
    if(f>=pad+wa+pad*0.5){ a.className='a in'; } else { a.style.left=Math.max(pad,f+pad*0.6)+'px'; }
    if(wq){ if(W-f>=pad+wq+pad*0.5){ } else if(f>=W-pad*0.4){ q.className='q in'; } else { q.className='q in'; q.style.right=(W-f+pad*0.6)+'px'; } } } }
var _rdB=render; render=function(d){ _rdB(d); ajustaBarras(); if(document.fonts&&document.fonts.ready) document.fonts.ready.then(ajustaBarras); };
window.addEventListener('resize',function(){ setTimeout(ajustaBarras,60); });
function fila("""
    assert s.count('function fila(')==1; s=s.replace('function fila(',BJ)
    if hz: H,F,P='calc(2.5 * var(--u))','calc(1.62 * var(--u))','calc(1 * var(--u))'
    elif gen: H,F,P='2.45vmin','1.62vmin','1vmin'
    else: H,F,P='2.15vmin','1.42vmin','0.9vmin'
    css='/* barra de ventas con cifras dentro */\n.pb2 { grid-column: span 2; position:relative; height:'+H+'; border-radius:99px; background: var(--line); overflow:hidden; font-size:'+F+'; line-height:1; }\n.pb2 i { position:absolute; top:0; bottom:0; left:0; background: var(--car); }\n.pb2 b { position:absolute; top:50%; transform:translateY(-50%); white-space:nowrap; font-weight:700; color: var(--fg); }\n.pb2 .a { left:'+P+'; } .pb2 .q { right:'+P+'; color: var(--grey); font-weight:600; }\n.pb2 b.in { color:#fff; }\n@media (max-width:700px){ .pb2 { height:4.4vmin; font-size:2.5vmin; } .pb2 .a { left:1.6vmin; } .pb2 .q { right:1.6vmin; } }\n</style>'
    assert s.count('</style>')==1; s=s.replace('</style>',css)
    x="OTRA+'?auto'"; assert s.count(x)==1,r; s=s.replace(x,"OTRA+'?auto'+(/[?&]quedan/.test(location.search)?'&quedan':'')")
    open(p,'w').write(s)
print('pruebas regeneradas')
