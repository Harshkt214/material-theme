"""20-Trade Challenge Tracker (.xlsx). Same style as journal/build.py.
Run: python3 build.py "20-Trade Challenge Tracker.xlsx" """
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from datetime import date

OUT = sys.argv[1]
F = "Arial"
HDR_DARK = PatternFill("solid", fgColor="1F2A44")
HDR_IN = PatternFill("solid", fgColor="FFD966")
IN_FILL = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="D0D4DC")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
RUPEE = '"₹"#,##0;("₹"#,##0);"-"'
RMULT = '0.00"R";(0.00"R");"-"'
PCT = '0.0%'
def font(bold=False, color="000000", size=10, italic=False):
    return Font(name=F, bold=bold, color=color, size=size, italic=italic)
def hdr(c, dark=True):
    c.font = font(True, "FFFFFF" if dark else "000000")
    c.fill = HDR_DARK if dark else HDR_IN
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BOX

wb = Workbook()
s = wb.active; s.title = "Start here"
s["A1"] = "20-Trade Challenge Tracker"; s["A1"].font = font(True, size=16)
s["A2"] = "Ek setup. 20 trades. Beech mein system nahi badalna. Result 20 ke baad dekho."
s["A2"].font = font(italic=True, color="555555")
s["A4"] = "Challenge ke rules"; s["A4"].font = font(True, size=12)
rules = [
    ("1", "Challenge tab ke upar apna EK setup likho (entry, SL, exit ka rule). 20 trades tak yahi setup."),
    ("2", "Har trade ke baad ek row bharo. Peele header wale columns aap bharte ho."),
    ("3", "R-multiple, win rate, average R aur total R apne aap bante hain (gehre neele header). Inhe mat chhuo."),
    ("4", "3 ya 5 loss lagatar aaye? Normal hai. Setup mat badlo. Ek trade ka result kuch saabit nahi karta."),
    ("5", "Har trade ka risk (₹) same rakho. Tabhi R ka hisaab saaf rahega."),
    ("6", "20 trades poore hone par right side ka Challenge summary dekho: average R plus mein hai ya minus mein? Tab faisla lo."),
    ("7", "Trade #1 wali row ek example hai. Padh kar delete kar do. Apni copy ke liye: File > Make a copy."),
]
for i, (n, t) in enumerate(rules):
    s.cell(row=5 + i, column=1, value=n).font = font(True)
    s.cell(row=5 + i, column=2, value=t).font = font()
s["A13"] = "Kyun 20 trades?"; s["A13"].font = font(True, size=12)
s["B14"] = "Mark Douglas (Trading in the Zone): edge bahut saare trades par dikhta hai, ek trade par nahi. Isliye ek sample tay karo aur result baad mein dekho."
s["A16"] = "Rang ka matlab"; s["A16"].font = font(True, size=12)
s["A17"].fill = HDR_IN; s["B17"] = "Peela = aap bharo"
s["A18"].fill = HDR_DARK; s["B18"] = "Gehra neela = formula, apne aap banta hai"
s["A20"] = "Educational use only. Not investment advice. @thetradingwizaard"
s["A20"].font = font(italic=True, color="888888")
s.column_dimensions["A"].width = 16; s.column_dimensions["B"].width = 100

C = wb.create_sheet("Challenge")
C["A1"] = "Mera setup (20 trades tak yahi):"; C["A1"].font = font(True, size=11)
C.merge_cells("D1:N1"); C["D1"] = "Example: 15-min chart par breakout ke baad retest par entry, SL retest candle ke neeche, exit 2R par"
C["D1"].fill = IN_FILL; C["D1"].font = font(color="0000FF", italic=True); C["D1"].border = BOX
cols = [("#", 5, False), ("Date", 12, True), ("Instrument", 24, True), ("Setup same tha?", 11, True),
        ("Buy/Sell", 9, True), ("Entry", 10, True), ("Stop loss", 10, True), ("Exit", 10, True),
        ("Risk (₹)", 11, True), ("P&L (₹)", 11, True), ("R-multiple", 11, False),
        ("Rule follow kiya?", 11, True), ("Emotion", 12, True), ("Note", 34, True)]
H = 3
for i, (h, w, is_in) in enumerate(cols):
    c = C.cell(row=H, column=i + 1, value=h); hdr(c, dark=not is_in)
    C.column_dimensions[c.column_letter].width = w
C.row_dimensions[H].height = 30
FIRST, LAST = H + 1, H + 20
for k, r in enumerate(range(FIRST, LAST + 1)):
    C.cell(row=r, column=1, value=k + 1).font = font(True, color="555555")
    C.cell(row=r, column=11, value=f'=IF(OR(I{r}="",J{r}="",I{r}=0),"",J{r}/I{r})').number_format = RMULT
    C.cell(row=r, column=2).number_format = "dd-mmm-yyyy"
    for cc in (9, 10): C.cell(row=r, column=cc).number_format = RUPEE
    for cc in range(1, 15): C.cell(row=r, column=cc).border = BOX
ex = [None, date(2026, 11, 21), "NIFTY 24500 CE (example, delete karo)", "Haan", "Buy", 120, 110, 140, 1000, 2000, None, "Haan", "Calm", "Plan ke hisaab se 2R par exit."]
for i, v in enumerate(ex):
    if v is not None:
        C.cell(row=FIRST, column=i + 1, value=v).font = font(italic=True, color="0000FF")
C.freeze_panes = C.cell(row=FIRST, column=3)
L = wb.create_sheet("Lists")
for col, (h, vals) in {"A": ("Haan/Nahi", ["Haan", "Nahi"]), "B": ("Buy/Sell", ["Buy", "Sell"]),
                       "C": ("Emotion", ["Calm", "Fear", "Greed", "FOMO", "Revenge", "Bored", "Overconfident"])}.items():
    hdr(L[f"{col}1"]); L[f"{col}1"] = h
    for i, v in enumerate(vals): L[f"{col}{i+2}"] = v
    L.column_dimensions[col].width = 16
for col, src in [("D", "=Lists!$A$2:$A$3"), ("E", "=Lists!$B$2:$B$3"), ("L", "=Lists!$A$2:$A$3"), ("M", "=Lists!$C$2:$C$8")]:
    dv = DataValidation(type="list", formula1=src, allow_blank=True); C.add_data_validation(dv); dv.add(f"{col}{FIRST}:{col}{LAST}")
green = PatternFill("solid", fgColor="D9F5E6"); red = PatternFill("solid", fgColor="FFE1E4")
rng = f"K{FIRST}:K{LAST}"
C.conditional_formatting.add(rng, CellIsRule(operator="greaterThan", formula=["0"], fill=green))
C.conditional_formatting.add(rng, CellIsRule(operator="lessThan", formula=["0"], fill=red))

# Summary block to the right
P, V = 16, 17  # columns P, Q
C.column_dimensions["O"].width = 3; C.column_dimensions["P"].width = 30; C.column_dimensions["Q"].width = 16
hdr(C.cell(row=H, column=P, value="Challenge summary")); hdr(C.cell(row=H, column=V, value="Value"))
J, K, Lc, D = f"J{FIRST}:J{LAST}", f"K{FIRST}:K{LAST}", f"L{FIRST}:L{LAST}", f"D{FIRST}:D{LAST}"
metrics = [
    ("Trades ho gaye", f'=COUNT({J})', "0"),
    ("Trades baaki (20 mein se)", f'=MAX(0,20-Q{FIRST})', "0"),
    ("Winning trades", f'=COUNTIF({J},">0")', "0"),
    ("Losing trades", f'=COUNTIF({J},"<0")', "0"),
    ("Win rate", f'=IF(Q{FIRST}=0,0,Q{FIRST+2}/Q{FIRST})', PCT),
    ("Average R (har trade)", f'=IF(COUNT({K})=0,0,AVERAGE({K}))', RMULT),
    ("Total R", f'=SUM({K})', RMULT),
    ("Average win (R)", f'=IF(COUNTIF({K},">0")=0,0,AVERAGEIF({K},">0"))', RMULT),
    ("Average loss (R)", f'=IF(COUNTIF({K},"<0")=0,0,AVERAGEIF({K},"<0"))', RMULT),
    ("Net P&L (₹)", f'=SUM({J})', RUPEE),
    ("Setup same raha (%)", f'=IF(COUNTA({D})=0,0,COUNTIF({D},"Haan")/COUNTA({D}))', PCT),
    ("Rule follow kiya (%)", f'=IF(COUNTA({Lc})=0,0,COUNTIF({Lc},"Haan")/COUNTA({Lc}))', PCT),
]
for i, (lab, f, fmt) in enumerate(metrics):
    r = FIRST + i
    C.cell(row=r, column=P, value=lab).font = font(True); C.cell(row=r, column=P).border = BOX
    c = C.cell(row=r, column=V, value=f); c.number_format = fmt; c.border = BOX; c.font = font(True)
sr = FIRST + len(metrics) + 1
C.cell(row=sr, column=P, value="Status").font = font(True, size=11)
C.merge_cells(start_row=sr + 1, start_column=P, end_row=sr + 3, end_column=V)
st = C.cell(row=sr + 1, column=P, value=f'=IF(Q{FIRST}<20,"Abhi "&Q{FIRST+1}&" trade baaki. Setup mat badlo.",IF(Q{FIRST+5}>0,"20 poore! Average R plus mein hai. Setup ko aur trades par test karo.","20 poore! Average R minus mein hai. Ab setup ya rules check karo."))')
st.font = font(True, color="1F2A44", size=11); st.alignment = Alignment(wrap_text=True, vertical="center")
st.fill = PatternFill("solid", fgColor="FFF2CC")
C.cell(row=sr + 5, column=P, value="Average R = har trade par average kitne R. Plus = 20 trades mein setup ne paisa banaya (costs ke baad bhi check karo).").font = font(italic=True, color="555555", size=9)
C.cell(row=sr + 5, column=P).alignment = Alignment(wrap_text=True, vertical="top")
C.merge_cells(start_row=sr + 5, start_column=P, end_row=sr + 8, end_column=V)
for ws in (s, C):
    ws.page_setup.orientation = "landscape"; ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
wb.move_sheet("Lists", offset=len(wb.sheetnames))
wb.save(OUT); print(wb.sheetnames)
