"""Risk aur Position Size Calculator (.xlsx). Same style as journal/build.py.
Run: python3 build.py "Risk Position Size Calculator.xlsx" """
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1]
F = "Arial"
HDR_DARK = PatternFill("solid", fgColor="1F2A44")
HDR_IN = PatternFill("solid", fgColor="FFD966")
IN_FILL = PatternFill("solid", fgColor="FFF2CC")
OUT_FILL = PatternFill("solid", fgColor="E3E8F2")
thin = Side(style="thin", color="D0D4DC")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
RUPEE = '"₹"#,##0;("₹"#,##0);"-"'
PRICE = '#,##0.00'
PCT = '0.00%'
def font(bold=False, color="000000", size=10, italic=False):
    return Font(name=F, bold=bold, color=color, size=size, italic=italic)
def hdr(c, dark=True):
    c.font = font(True, "FFFFFF" if dark else "000000")
    c.fill = HDR_DARK if dark else HDR_IN
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BOX

wb = Workbook()
s = wb.active; s.title = "Start here"
s["A1"] = "Risk aur Position Size Calculator"; s["A1"].font = font(True, size=16)
s["A2"] = "Pehle risk tay karo, phir quantity. Mood se nahi, formula se."; s["A2"].font = font(italic=True, color="555555")
s["A4"] = "Kaise use karein"; s["A4"].font = font(True, size=12)
steps = [
    ("1", "Calculator tab mein peeli cells bharo: capital, risk per trade %, entry, stop loss, lot size."),
    ("2", "Quantity aur lots apne aap bante hain: Risk ₹ / (entry - SL) = quantity; quantity / lot size = lots (neeche round)."),
    ("3", "Lots 0 aaye? Matlab 1 lot ka risk bhi tumhari limit se zyada hai. Trade skip karo ya SL/instrument dobara socho."),
    ("4", "Lot size apne broker ya exchange ki website se check karo. Ye badalta rehta hai. Sheet mein diya number sirf example hai."),
    ("5", "Drawdown tab dekho: capital jitna girta hai, wapas aane ke liye utna hi zyada % chahiye."),
    ("6", "Apni copy ke liye: File > Make a copy."),
]
for i, (n, t) in enumerate(steps):
    s.cell(row=5 + i, column=1, value=n).font = font(True)
    s.cell(row=5 + i, column=2, value=t).font = font()
s["A12"] = "Rang ka matlab"; s["A12"].font = font(True, size=12)
s["A13"].fill = IN_FILL; s["B13"] = "Peela = aap bharo"
s["A14"].fill = OUT_FILL; s["B14"] = "Neela-grey = formula, apne aap banta hai"
s["A16"] = "Bahut se traders ek trade mein capital ka 1 se 2% risk rakhte hain. Ye common practice hai, niyam nahi."
s["A17"] = "Costs (brokerage, taxes, slippage) is calculator mein shaamil nahi hain."
s["A19"] = "Educational use only. Not investment advice. @thetradingwizaard"; s["A19"].font = font(italic=True, color="888888")
s.column_dimensions["A"].width = 16; s.column_dimensions["B"].width = 105

C = wb.create_sheet("Calculator")
C["A1"] = "Position size calculator"; C["A1"].font = font(True, size=14)
C["A2"] = "Peeli cells bharo. Baaki apne aap."; C["A2"].font = font(italic=True, color="555555")
hdr(C["A4"]); C["A4"] = "Input"; hdr(C["B4"]); C["B4"] = "Value"; hdr(C["C4"]); C["C4"] = "Note"
inputs = [
    ("Capital (₹)", 100000, RUPEE, "Trading account mein kitna paisa (example)"),
    ("Risk per trade (%)", 0.01, PCT, "Ek trade mein capital ka kitna % risk (example: 1%)"),
    ("Entry price", 200, PRICE, "Jahan buy/sell karoge (example)"),
    ("Stop loss price", 190, PRICE, "Jahan galat saabit hoge (example)"),
    ("Lot size", 50, "0", "Example number. Asli lot size broker/exchange se check karo"),
]
for i, (lab, v, fmt, note) in enumerate(inputs):
    r = 5 + i
    C.cell(row=r, column=1, value=lab).font = font(True); C.cell(row=r, column=1).border = BOX
    c = C.cell(row=r, column=2, value=v); c.number_format = fmt; c.fill = IN_FILL; c.font = font(color="0000FF"); c.border = BOX
    C.cell(row=r, column=3, value=note).font = font(italic=True, color="555555")
dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="0.1", showErrorMessage=True,
                    errorTitle="Risk %", error="0% se 10% ke beech daalo (jaise 1% = 0.01)")
C.add_data_validation(dv); dv.add("B6")

hdr(C["A11"]); C["A11"] = "Result"; hdr(C["B11"]); C["B11"] = "Value"; hdr(C["C11"]); C["C11"] = "Formula"
outs = [
    ("Risk per trade (₹)", "=B5*B6", RUPEE, "Capital × risk %"),
    ("Risk per unit (₹)", "=ABS(B7-B8)", PRICE, "|Entry − SL| (buy ya sell, dono chalega)"),
    ("Quantity (max)", '=IF(B13=0,0,ROUNDDOWN(B12/B13,0))', "#,##0", "Risk ₹ / risk per unit, neeche round"),
    ("Lots", '=IF(OR(B9="",B9=0),0,ROUNDDOWN(B14/B9,0))', "#,##0", "Quantity / lot size, neeche round"),
    ("Final quantity (lots × lot size)", "=B15*B9", "#,##0", "Itni quantity ka order"),
    ("Asli risk agar SL lage (₹)", "=B16*B13", RUPEE, "Final quantity × risk per unit"),
    ("Asli risk (% of capital)", "=IF(B5=0,0,B17/B5)", PCT, "Limit se kam ya barabar hona chahiye"),
    ("1 lot ka risk (₹)", "=B9*B13", RUPEE, "Agar ye risk ₹ se zyada hai, lots = 0"),
    ("Position value (₹)", "=B16*B7", RUPEE, "Final quantity × entry (margin alag hota hai)"),
    ("Target at 2R (price)", '=IF(B7>=B8,B7+2*B13,B7-2*B13)', PRICE, "Entry se 2 × risk per unit door (example target)"),
]
for i, (lab, f, fmt, note) in enumerate(outs):
    r = 12 + i
    C.cell(row=r, column=1, value=lab).font = font(True); C.cell(row=r, column=1).border = BOX
    c = C.cell(row=r, column=2, value=f); c.number_format = fmt; c.fill = OUT_FILL; c.font = font(True); c.border = BOX
    C.cell(row=r, column=3, value=note).font = font(italic=True, color="555555")
C["A23"] = "Faisla"; C["A23"].font = font(True, size=12)
C.merge_cells("A24:C25")
C["A24"] = ('=IF(B13=0,"Entry aur SL alag hone chahiye.",IF(B15=0,"1 lot ka risk ("&TEXT(B19,"#,##0")&") tumhari limit ("&TEXT(B12,"#,##0")&") se zyada hai. Ye trade skip karo.",'
            '"Order: "&B15&" lot = "&TEXT(B16,"#,##0")&" quantity. SL lage to loss lagbhag ₹"&TEXT(B17,"#,##0")&"."))')
C["A24"].font = font(True, size=12, color="1F2A44"); C["A24"].fill = PatternFill("solid", fgColor="FFF2CC")
C["A24"].alignment = Alignment(wrap_text=True, vertical="center")
C.column_dimensions["A"].width = 34; C.column_dimensions["B"].width = 18; C.column_dimensions["C"].width = 58

D = wb.create_sheet("Drawdown")
D["A1"] = "Drawdown recovery table"; D["A1"].font = font(True, size=14)
D["A2"] = "Capital jitna girta hai, wapas aane ke liye utna hi zyada % chahiye. Formula: loss / (1 − loss)."
D["A2"].font = font(italic=True, color="555555")
for j, h in enumerate(["Capital ka loss", "Wapas aane ke liye chahiye", "Example capital (B16) mein se bacha", "Wapas pahunchne ke liye kamana"]):
    hdr(D.cell(row=4, column=1 + j, value=h))
D.row_dimensions[4].height = 30
for k, L in enumerate([0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.75, 0.90]):
    r = 5 + k
    D.cell(row=r, column=1, value=L).number_format = "0%"
    D.cell(row=r, column=2, value=f"=A{r}/(1-A{r})").number_format = "0.0%"
    D.cell(row=r, column=3, value=f"=$B$16*(1-A{r})").number_format = RUPEE
    D.cell(row=r, column=4, value=f"=$B$16-C{r}").number_format = RUPEE
    for cc in range(1, 5): D.cell(row=r, column=cc).border = BOX
    D.cell(row=r, column=1).fill = IN_FILL; D.cell(row=r, column=1).font = font(color="0000FF")
D["A16"] = "Example capital (₹)"; D["A16"].font = font(True)
D["B16"] = 100000; D["B16"].number_format = RUPEE; D["B16"].fill = IN_FILL; D["B16"].font = font(color="0000FF")
D["A18"] = "Apna % try karo (A column mein koi bhi loss % daalo)."; D["A18"].font = font(italic=True, color="555555")
for col, w in zip("ABCD", (20, 26, 28, 30)): D.column_dimensions[col].width = w
for ws in (s, C, D):
    ws.page_setup.orientation = "landscape"; ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
wb.save(OUT); print(wb.sheetnames)
