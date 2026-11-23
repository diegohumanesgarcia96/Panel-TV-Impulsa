# Regenera las páginas de prueba a partir de las definitivas: mismas páginas + fila de terceros de Sevilla (pendiente de datos de Alfonso)
FT="function filaT(t){ return '<div class=\"pr\"><div class=\"pn\"><div class=\"pnt\"><span class=\"pt\">'+nomb(t.nombre)+'</span><span class=\"pl\">'+esc(t.localidad)+'</span></div></div><div class=\"pf\">'+esc(t.fase||'Comercialización')+'</div><div></div><div class=\"pv\">'+fmtN(t.viviendas)+'<span>\\u00a0viv.</span></div></div>'; }\nfunction render(d){"
M={'index.html':('prueba.html',"OTRA='horizontal.html'","OTRA='prueba-horizontal.html'"),'horizontal.html':('prueba-horizontal.html',"OTRA='index.html'","OTRA='prueba.html'"),'general.html':('prueba-general.html',"OTRA='general-horizontal.html'","OTRA='prueba-general-horizontal.html'"),'general-horizontal.html':('prueba-general-horizontal.html',"OTRA='general.html'","OTRA='prueba-general.html'")}
for r,(p,a,b) in M.items():
    s=open(r).read(); assert a in s; s=s.replace(a,b)
    if r in('index.html','horizontal.html'): assert s.count('var SOLO_OBJ=false;')==1; s=s.replace('var SOLO_OBJ=false;','var SOLO_OBJ=true;')
    if r!='index.html':
        assert s.count('function render(d){')==1; s=s.replace('function render(d){',FT)
        if 'horizontal' in r:
            x="p.viviendas>0&&p.vendidas>=p.viviendas,p.maps,entrega(p)); });\n"; assert s.count(x)==1,r
            s=s.replace(x,x+"    var nt=0; if(z.terceros){ rows+=filaT(z.terceros); nt=1; }\n")
            assert s.count('z.promos.length+1.2')==2; s=s.replace('z.promos.length+1.2','z.promos.length+nt+1.2')
        else:
            x="    h+='<section style=\"flex:'+(z.promos.length+1.3)+'\">"; assert s.count(x)==1
            s=s.replace(x,"    var nt=0; if(z.terceros){ rows+=filaT(z.terceros); nt=1; }\n    h+='<section style=\"flex:'+(z.promos.length+nt+1.3)+'\">")
    open(p,'w').write(s)
print('pruebas regeneradas')
