#!/usr/bin/env python3
"""Panel de control del grupo en Excel con formato Impulsa, generado desde datos.json.
Uso: python3 panel_excel.py <Plantilla_Impulsa.xlsx> <salida.xlsx>"""
import json, sys, datetime, copy
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import DataBarRule, FormulaRule
from openpyxl.utils import get_column_letter

TPL, OUT = sys.argv[1], sys.argv[2]
d = json.load(open('datos.json'))
GREY, CAR, SILVER, LINE, ZEBRA, OK, BAD = '82817E', 'D68842', 'C2C0BE', 'E8E7E6', 'F5F4F3', '155724', '721C24'
F = 'Poppins'
f_body = Font(name=F, size=10, color=GREY); f_bold = Font(name=F, size=10, bold=True, color=GREY)
f_hdr = Font(name=F, size=10, bold=True, color='FFFFFF'); fill_hdr = PatternFill('solid', fgColor=GREY)
fill_car = PatternFill('solid', fgColor=CAR); fill_zebra = PatternFill('solid', fgColor=ZEBRA); fill_white = PatternFill('solid', fgColor='FFFFFF')
thin = Side(style='thin', color=LINE); border = Border(top=thin, bottom=thin, left=thin, right=thin)
center = Alignment(horizontal='center', vertical='center'); left = Alignment(horizontal='left', vertical='center'); right = Alignment(horizontal='right', vertical='center')
hoy = datetime.date.today()
upd = datetime.date.fromisoformat(d['actualizado'])

wb = load_workbook(TPL)
# ---------------- Portada ----------------
p = wb['Portada']
p['C4'] = 'PANEL DE CONTROL'
p['C7'] = 'Grupo Impulsa · promociones en curso en España y Colombia'
p['D9'] = 'Panel de control del grupo'
p['D10'] = upd.strftime('%d/%m/%Y')
p['C11'] = 'Datos a:'; p['D11'] = upd.strftime('%d/%m/%Y')
p['D12'] = '1.0'; p['D13'] = 'Vigente'

# ---------------- Panel (sustituye a Datos) ----------------
ws = wb['Datos']; ws.title = 'Panel'
for row in ws.iter_rows(min_row=6, max_row=ws.max_row):
    for c in row: c.value = None; c.fill = PatternFill(); c.border = Border(); c.font = f_body
for m in list(ws.merged_cells.ranges):
    if m.min_row >= 6: ws.unmerge_cells(str(m))
ws['C4'] = 'Panel de control · Grupo Impulsa'
ws['C5'] = f"Promociones en curso en España y Colombia · datos a {upd.strftime('%d/%m/%Y')}"
widths = {'A': 3, 'B': 3, 'C': 38, 'D': 24, 'E': 18, 'F': 11, 'G': 11, 'H': 11, 'I': 16, 'J': 3}
for k, v in widths.items(): ws.column_dimensions[k].width = v

# KPIs
viv_es = sum(pr['viviendas'] for z in d['zonas'] for pr in z['promos']); vend_es = sum(pr['vendidas'] for z in d['zonas'] for pr in z['promos'])
obra_es = sum(pr['viviendas'] for z in d['zonas'] for pr in z['promos'] if pr['obra']); nprom_es = sum(1 for z in d['zonas'] for pr in z['promos'] if not pr['espera'])
viv_co = sum(c['viviendas'] for c in d['colombia']); vend_co = sum(c['ventas'] for c in d['colombia']); obra_co = sum(c['obra_viv'] for c in d['colombia']); nprom_co = len(d['colombia'])
kpis = [('Viviendas actuales en promoción', viv_es + viv_co, f'{viv_es:,} ESP + {viv_co:,} COL'),
        ('Viviendas actuales vendidas', vend_es + vend_co, f'{vend_es:,} ESP + {vend_co:,} COL · {(vend_es+vend_co)/(viv_es+viv_co):.0%}'),
        ('Viviendas actuales en obra', obra_es + obra_co, f'{obra_es:,} ESP + {obra_co:,} COL'),
        ('Promociones actuales', nprom_es + nprom_co, f'{nprom_es} ESP + {nprom_co} COL')]
r = 7
for i, (lab, val, sub) in enumerate(kpis):
    c1, c2 = ('C', 'D') if i % 2 == 0 else ('E', 'G')
    rr = r if i < 2 else r + 3
    ws.merge_cells(f'{c1}{rr}:{c2}{rr}'); ws.merge_cells(f'{c1}{rr+1}:{c2}{rr+1}')
    a = ws[f'{c1}{rr}']; a.value = lab.upper(); a.font = Font(name=F, size=9, bold=True, color='FFFFFF'); a.fill = fill_car; a.alignment = center
    b = ws[f'{c1}{rr+1}']; b.value = f'{val:,}'.replace(',', '.') + '   ·   ' + sub.replace(',', '.'); b.font = Font(name=F, size=12, bold=True, color=GREY); b.fill = fill_zebra; b.alignment = center
    ws.row_dimensions[rr].height = 18; ws.row_dimensions[rr + 1].height = 26
# ajustar: KPIs en 4 bloques horizontales (C-D, E-F, G-H, I) es estrecho; usamos 2x2 en C-D y E-F + G-H, I vacío -> simplificar a 2x2 en C:D y E:F
r = 13
heads = ['Promoción', 'Localidad', 'Fase', 'Viviendas', 'Vendidas', '% vendido', 'Avance ventas']
for j, h in enumerate(heads):
    c = ws.cell(row=r, column=3 + j, value=h); c.font = f_hdr; c.fill = fill_hdr; c.alignment = center; c.border = border
ws.row_dimensions[r].height = 20
r += 1
first_data = r
for z in d['zonas']:
    tv = sum(pr['viviendas'] for pr in z['promos']); ts = sum(pr['vendidas'] for pr in z['promos'])
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=9)
    c = ws.cell(row=r, column=3, value=f"{z['zona'].upper()}   ·   {tv} viv. · {ts} vendidas"); c.font = Font(name=F, size=10, bold=True, color=CAR); c.alignment = left
    c.fill = fill_white
    for j in range(7): ws.cell(row=r, column=3 + j).border = Border(bottom=Side(style='medium', color=CAR))
    r += 1
    for k, pr in enumerate(z['promos']):
        fill = fill_zebra if k % 2 else fill_white
        pct = pr['vendidas'] / pr['viviendas'] if pr['viviendas'] else 0
        vals = [pr['nombre'], pr['localidad'], pr['fase'], pr['viviendas'], pr['vendidas'], pct, pct]
        for j, v in enumerate(vals):
            c = ws.cell(row=r, column=3 + j, value=v); c.font = f_body; c.fill = fill; c.border = border
            c.alignment = left if j < 3 else center
        ws.cell(row=r, column=3).font = f_bold
        ws.cell(row=r, column=8).number_format = '0%'; ws.cell(row=r, column=9).number_format = ';;;'  # barra sin número
        fase_cell = ws.cell(row=r, column=5)
        if pr['cls'] == 'ok': fase_cell.font = Font(name=F, size=10, bold=True, color=OK)
        elif pr['cls'] == 'warn': fase_cell.font = Font(name=F, size=10, bold=True, color='8D5223')
        elif pr['cls'] == 'mut': fase_cell.font = Font(name=F, size=10, color=SILVER)
        r += 1
last_es = r - 1
# Colombia
ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=9)
c = ws.cell(row=r, column=3, value='COLOMBIA   ·   Hábitat Colombia · ventas sobre punto de equilibrio'); c.font = Font(name=F, size=10, bold=True, color=CAR); c.alignment = left
for j in range(7): ws.cell(row=r, column=3 + j).border = Border(bottom=Side(style='medium', color=CAR))
r += 1
for k, co in enumerate(d['colombia']):
    fill = fill_zebra if k % 2 else fill_white
    pct = co['ventas'] / co['pe'] if co['pe'] else 0
    vals = [co['nombre'], co['localidad'], co['estado'], f"{co['viviendas']} · PE {co['pe']}", f"{co['ventas']} / {co['pe']}", pct, pct]
    for j, v in enumerate(vals):
        c = ws.cell(row=r, column=3 + j, value=v); c.font = f_body; c.fill = fill; c.border = border; c.alignment = left if j < 3 else center
    ws.cell(row=r, column=3).font = f_bold
    ws.cell(row=r, column=8).number_format = '0%'; ws.cell(row=r, column=9).number_format = ';;;'
    if co['obra_viv']: ws.cell(row=r, column=5).font = Font(name=F, size=10, bold=True, color=OK)
    r += 1
last_co = r - 1
ws.conditional_formatting.add(f'I{first_data}:I{last_co}', DataBarRule(start_type='num', start_value=0, end_type='num', end_value=1, color=CAR, showValue=False))
r += 1
c = ws.cell(row=r, column=3, value='Fase en verde = en obra · en marrón = licencia · en gris = en espera. Colombia: ventas sobre el punto de equilibrio (PE) de cada torre/fase. Fuente: acta semanal de coordinadores y seguimiento de Hábitat Colombia.'); c.font = Font(name=F, size=8, color=SILVER)
ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=9); c.alignment = Alignment(wrap_text=True, vertical='top'); ws.row_dimensions[r].height = 26
ws.sheet_view.showGridLines = False
ws.print_area = f'A1:J{r+1}'; ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 1; ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.freeze_panes = 'C14'
for rr in range(13, r + 1): ws.row_dimensions[rr].height = 16

# ---------------- Hitos (sustituye a Seguimiento) ----------------
hs = wb['Seguimiento']; hs.title = 'Hitos'
for row in hs.iter_rows(min_row=7, max_row=hs.max_row):
    for c in row: c.value = None; c.fill = PatternFill(); c.border = Border(); c.font = f_body
hs['C4'] = 'Próximos hitos del grupo'
heads = ['Nº', 'Hito', 'Ámbito', 'Fecha', 'Días', 'Estado', 'Tipo']
for j, h in enumerate(heads):
    c = hs.cell(row=6, column=3 + j, value=h); c.font = f_hdr; c.fill = fill_hdr; c.alignment = center; c.border = border
hitos = sorted(d['hitos'], key=lambda h: h['fecha'])
hitos = [h for h in hitos if (datetime.date.fromisoformat(h['fecha']) - hoy).days >= -7]
r = 7
for k, h in enumerate(hitos):
    f = datetime.date.fromisoformat(h['fecha']); dias = (f - hoy).days
    estado = 'Hecho' if dias < 0 else ('Hoy' if dias == 0 else ('Esta semana' if dias <= 7 else 'Pendiente'))
    fill = fill_zebra if k % 2 else fill_white
    vals = [k + 1, h['hito'], h['ambito'], f, dias, estado, h['tipo']]
    for j, v in enumerate(vals):
        c = hs.cell(row=r, column=3 + j, value=v); c.font = f_body; c.fill = fill; c.border = border; c.alignment = left if j in (1, 2) else center
    hs.cell(row=r, column=6).number_format = 'dd/mm/yyyy'
    e = hs.cell(row=r, column=8); e.font = Font(name=F, size=9.5, bold=True, color={'Hecho': OK, 'Hoy': BAD, 'Esta semana': '856404', 'Pendiente': GREY}[estado])
    e.fill = PatternFill('solid', fgColor={'Hecho': 'D4EDDA', 'Hoy': 'FDE8E8', 'Esta semana': 'FFF3CD', 'Pendiente': fill.fgColor.rgb}[estado])
    r += 1
hs.column_dimensions['D'].width = 62; hs.column_dimensions['E'].width = 24; hs.column_dimensions['F'].width = 12; hs.column_dimensions['G'].width = 8; hs.column_dimensions['H'].width = 13; hs.column_dimensions['I'].width = 14
hs.sheet_view.showGridLines = False
hs.print_area = f'A1:J{r}'; hs.page_setup.orientation = 'landscape'; hs.page_setup.fitToWidth = 1; hs.page_setup.fitToHeight = 0; hs.sheet_properties.pageSetUpPr.fitToPage = True
c = hs.cell(row=r + 1, column=3, value=f"Días contados desde {hoy.strftime('%d/%m/%Y')}. Los hitos de más de una semana atrás desaparecen de la lista."); c.font = Font(name=F, size=8, color=SILVER)

p.print_area = 'A1:F40'; p.page_setup.fitToWidth = 1; p.page_setup.fitToHeight = 1; p.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(OUT)
print('ok', OUT)
