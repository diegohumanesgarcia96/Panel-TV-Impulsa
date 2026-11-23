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
    # PRUEBA 23/11 13:38 (Miguel): vendidas y restantes DENTRO de la barra; se quita el número de la derecha
    hz='horizontal' in r; gen='general' in r
    x="<div class=\"pb\"><i style=\"width:'+Math.max(0,Math.min(100,Math.round(pct)))+'%\"></i></div><div class=\"pv\">'+s+'<span>/'+v+'</span></div></div>'"
    assert s.count(x)==1,r; s=s.replace(x,"'+barra(pct,s,v)+'</div>'")
    BJ="function barra(pct,s,v){ var p=Math.max(0,Math.min(100,Math.round(pct))), ns=+String(s).replace(/\\./g,''), nv=+String(v).replace(/\\./g,''), q=Math.max(0,nv-ns); var t='<div class=\"bt\"><b>'+fmtN(ns)+'</b><b>'+(q>0?fmtN(q):'')+'</b></div>'; return '<div class=\"pb2\" style=\"--p:'+p+'\" title=\"'+fmtN(ns)+' vendidas · '+fmtN(q)+' disponibles\">'+t+(p>0?'<i>'+t+'</i>':'')+'</div>'; }\nfunction fila("
    assert s.count('function fila(')==1; s=s.replace('function fila(',BJ)
    if hz: H,F,P='calc(2.5 * var(--u))','calc(1.62 * var(--u))','calc(1 * var(--u))'
    elif gen: H,F,P='2.45vmin','1.62vmin','1vmin'
    else: H,F,P='2.15vmin','1.42vmin','0.9vmin'
    css='/* barra de ventas con cifras dentro: capa gris con texto oscuro y, encima, el relleno naranja recortado con el mismo texto en blanco */\n.pb2 { grid-column: span 2; position:relative; height:'+H+'; border-radius:99px; background: var(--line); overflow:hidden; font-size:'+F+'; font-weight:700; line-height:1; }\n.pb2 .bt { position:absolute; top:0; bottom:0; left:0; width:100%; display:flex; justify-content:space-between; align-items:center; padding:0 '+P+'; box-sizing:border-box; color: var(--fg); white-space:nowrap; }\n.pb2 .bt b:last-child { color: var(--grey); font-weight:600; }\n.pb2 i { position:absolute; top:0; bottom:0; left:0; width:calc(var(--p) * 1%); background: var(--car); overflow:hidden; font-style:normal; }\n.pb2 i .bt { width:calc(100% * 100 / var(--p)); color:#fff; } .pb2 i .bt b:last-child { color:#fff; }\n@media (max-width:700px){ .pb2 { height:4.4vmin; font-size:2.5vmin; } .pb2 .bt { padding:0 1.6vmin; } }\n</style>'
    assert s.count('</style>')==1; s=s.replace('</style>',css)
    open(p,'w').write(s)
print('pruebas regeneradas')
