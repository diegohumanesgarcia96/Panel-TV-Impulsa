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
    # PRUEBA 23/11: logo de la empresa junto al nombre de cada zona (color; con ?gris en la dirección, en gris)
    hz='horizontal' in r
    LZ="function logoZ(z){ var M={'Madrid':['madrid',1],'Aragón':['aragon',1],'Cataluña':['cataluna',1],'Andalucía':['andalucia',1],'Colombia':['colombia',0.4]}, m=M[z]; return m?'<img class=\"zl\" alt=\"\" style=\"--k:'+m[1]+'\" src=\"logos/'+m[0]+'.png\">':''; }\nif(/[?&]gris/.test(location.search)) document.documentElement.className+=' gris';\nfunction render(d){"
    assert s.count('function render(d){')==1; s=s.replace('function render(d){',LZ)
    x="<h2>'+esc(z.zona)+'<span>"; assert s.count(x)==1,r; s=s.replace(x,"<h2>'+esc(z.zona)+logoZ(z.zona)+'<span>")
    x="<h2>Colombia<span>"; assert s.count(x)==1,r; s=s.replace(x,"<h2>Colombia'+logoZ('Colombia')+'<span>")
    U='calc(2.6 * var(--u) * var(--k))' if hz else 'calc(2.35vmin * var(--k))'
    G='calc(1 * var(--u))' if hz else '0.9vmin'
    css='.zl { height:'+U+'; width:auto; flex:0 0 auto; align-self:center; margin:-0.5em auto -0.5em '+G+'; } html.gris .zl { filter: grayscale(1) opacity(.6); }\n@media (prefers-color-scheme: dark) { .zl, html.gris .zl { filter: brightness(0) invert(1) opacity(.8); } }\n@media (max-width:700px){ .zl { height: calc(2.6vmin * var(--k)); } }\n</style>'
    assert s.count('</style>')==1; s=s.replace('</style>',css)
    open(p,'w').write(s)
print('pruebas regeneradas')
