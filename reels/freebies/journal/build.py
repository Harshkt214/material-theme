import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from datetime import date

OUT = sys.argv[1]
PUBLIC = "--public" in sys.argv  # audience version: no internal Freebies tab
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
s = wb.active
s.title = "Start here"
s["A1"] = "Free Trading Journal"; s["A1"].font = font(True, size=16)
s["A2"] = "Har trade likho, har hafte Summary dekho. Galtiyan numbers mein dikhengi."
s["A2"].font = font(italic=True, color="555555")
steps = [
    ("1", "Settings tab mein apna capital, risk per trade % aur daily max loss bharo (peeli cells)."),
    ("2", "Har trade ke baad Journal tab mein ek row bharo. Peele header wale columns aap bharte ho."),
    ("3", "# aur R-multiple apne aap bante hain (gehre neele header wale columns). Inhe mat chhuo."),
    ("4", "Row 2 ek example hai. Padh kar delete kar do."),
    ("5", "Har hafte Summary tab dekho: win rate, average R, aur rule todne par kitna paisa gaya."),
    ("6", "Apni copy ke liye: File > Make a copy."),
]
s["A4"] = "Kaise use karein"; s["A4"].font = font(True, size=12)
for i, (n, t) in enumerate(steps):
    s.cell(row=5 + i, column=1, value=n).font = font(True)
    s.cell(row=5 + i, column=2, value=t).font = font()
s["A12"] = "Rang ka matlab"; s["A12"].font = font(True, size=12)
s["A13"].fill = HDR_IN; s["B13"] = "Peela = aap bharo"
s["A14"].fill = HDR_DARK; s["B14"] = "Gehra neela = formula, apne aap banta hai"
s["A16"] = "Educational use only. Not investment advice."
s["A16"].font = font(italic=True, color="888888")
s.column_dimensions["A"].width = 16; s.column_dimensions["B"].width = 95

L = wb.create_sheet("Lists")
lists = {
    "A": ("Buy/Sell", ["Buy", "Sell"]),
    "B": ("Haan/Nahi", ["Haan", "Nahi"]),
    "C": ("Emotion", ["Calm", "Fear", "Greed", "FOMO", "Revenge", "Bored", "Overconfident"]),
    "D": ("Galti", ["Koi nahi", "SL hataya", "Revenge trade", "Overtrading", "Averaging down", "Jaldi exit", "Plan ke bina trade", "Size bada liya"]),
}
for col, (h, vals) in lists.items():
    hdr(L[f"{col}1"]); L[f"{col}1"] = h
    for i, v in enumerate(vals):
        L[f"{col}{i+2}"] = v; L[f"{col}{i+2}"].font = font()
    L.column_dimensions[col].width = 22

st = wb.create_sheet("Settings", 1)
st["A1"] = "Settings"; st["A1"].font = font(True, size=14)
rows = [("Starting capital (₹)", 100000, RUPEE, True), ("Risk per trade (%)", 0.01, PCT, True),
        ("Risk per trade (₹)", "=B3*B4", RUPEE, False), ("Daily max loss (₹)", 2000, RUPEE, True)]
for i, (lab, val, fmt, is_in) in enumerate(rows):
    r = 3 + i
    st.cell(row=r, column=1, value=lab).font = font(True)
    c = st.cell(row=r, column=2, value=val); c.number_format = fmt; c.border = BOX
    if is_in:
        c.fill = IN_FILL; c.font = font(color="0000FF")
        st.cell(row=r, column=3, value="Source: aapka apna input (example value, apna number daalo)").font = font(italic=True, color="555555")
st["A8"] = "Bahut se traders ek trade mein capital ka 1 se 2% risk rakhte hain. Ye niyam nahi, common practice hai."

J = wb.create_sheet("Journal", 2)
cols = [("#", 6, False), ("Date", 12, True), ("Instrument", 26, True), ("Buy/Sell", 10, True),
        ("Setup", 18, True), ("Entry reason", 30, True), ("Exit reason", 24, True),
        ("Risk (₹)", 12, True), ("P&L (₹)", 12, True), ("R-multiple", 12, False),
        ("Rule follow kiya?", 13, True), ("Emotion", 14, True), ("Galti", 18, True), ("Lesson", 36, True)]
for i, (h, w, is_in) in enumerate(cols):
    c = J.cell(row=1, column=i + 1, value=h); hdr(c, dark=not is_in)
    J.column_dimensions[c.column_letter].width = w
J.freeze_panes = "C2"
N = 101
for r in range(2, N + 1):
    J.cell(row=r, column=1, value=f'=IF(C{r}="","",ROW()-1)')
    J.cell(row=r, column=10, value=f'=IF(OR(H{r}="",I{r}="",H{r}=0),"",I{r}/H{r})')
    J.cell(row=r, column=2).number_format = "dd-mmm-yyyy"
    for cc in (8, 9): J.cell(row=r, column=cc).number_format = RUPEE
    J.cell(row=r, column=10).number_format = RMULT
ex = [None, date(2026, 11, 3), "NIFTY 24500 CE (example, delete karo)", "Buy", "Breakout retest",
      "Resistance tooti, retest par entry", "SL hit", 1000, -1000, None, "Haan", "Calm", "Koi nahi",
      "Setup sahi tha. Loss business ka kharcha hai."]
for i, v in enumerate(ex):
    if v is not None:
        J.cell(row=2, column=i + 1, value=v).font = font(italic=True, color="0000FF")
for col, src in [("D", "=Lists!$A$2:$A$3"), ("K", "=Lists!$B$2:$B$3"), ("L", "=Lists!$C$2:$C$8"), ("M", "=Lists!$D$2:$D$9")]:
    dv = DataValidation(type="list", formula1=src, allow_blank=True)
    J.add_data_validation(dv); dv.add(f"{col}2:{col}{N}")

S = wb.create_sheet("Summary", 3)
S["A1"] = "Summary"; S["A1"].font = font(True, size=14)
metrics = [
    ("Total trades", "=COUNTA(Journal!C:C)-1", "0"),
    ("Winning trades", '=COUNTIF(Journal!I:I,">0")', "0"),
    ("Losing trades", '=COUNTIF(Journal!I:I,"<0")', "0"),
    ("Win rate", "=IF(B4=0,0,B5/B4)", PCT),
    ("Net P&L (₹)", "=SUM(Journal!I:I)", RUPEE),
    ("Average R", "=IF(COUNT(Journal!J:J)=0,0,AVERAGE(Journal!J:J))", RMULT),
    ("Average win (₹)", '=IF(B5=0,0,AVERAGEIF(Journal!I:I,">0"))', RUPEE),
    ("Average loss (₹)", '=IF(B6=0,0,AVERAGEIF(Journal!I:I,"<0"))', RUPEE),
    ("Trades with rule answer", "=COUNTA(Journal!K:K)-1", "0"),
    ("Rule follow kiya (%)", '=IF(B12=0,0,COUNTIF(Journal!K:K,"Haan")/B12)', PCT),
    ("P&L jab rule follow kiya (₹)", '=SUMIF(Journal!K:K,"Haan",Journal!I:I)', RUPEE),
    ("P&L jab rule toda (₹)", '=SUMIF(Journal!K:K,"Nahi",Journal!I:I)', RUPEE),
    ("Current capital (₹)", "=Settings!B3+B8", RUPEE),
    ("Daily max loss (₹)", "=Settings!B6", RUPEE),
]
hdr(S["A3"]); S["A3"] = "Metric"; hdr(S["B3"]); S["B3"] = "Value"
for i, (lab, f, fmt) in enumerate(metrics):
    S.cell(row=4 + i, column=1, value=lab).font = font(True)
    c = S.cell(row=4 + i, column=2, value=f); c.number_format = fmt
def breakdown(start_row, title, list_col, n, journal_col):
    S.cell(row=start_row, column=1, value=title).font = font(True, size=12)
    for j, h in enumerate([title.split(" ")[0], "Trades", "P&L (₹)"]):
        hdr(S.cell(row=start_row + 1, column=1 + j, value=h))
    for k in range(n):
        r = start_row + 2 + k
        S.cell(row=r, column=1, value=f"=Lists!{list_col}{k+2}")
        S.cell(row=r, column=2, value=f"=COUNTIF(Journal!{journal_col}:{journal_col},A{r})")
        S.cell(row=r, column=3, value=f"=SUMIF(Journal!{journal_col}:{journal_col},A{r},Journal!I:I)").number_format = RUPEE
    return start_row + 2 + n + 1
nxt = breakdown(19, "Emotion ke hisaab se", "C", 7, "L")
breakdown(nxt, "Galti ke hisaab se", "D", 8, "M")
S.column_dimensions["A"].width = 30

wb.move_sheet("Lists", offset=len(wb.sheetnames))
wb.save(OUT)
print(wb.sheetnames)
