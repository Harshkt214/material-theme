# Risk & Position Size Calculator (freebie: RISK)

Single static page (`index.html` + `favicon.svg`). No build, no server, so it can be hosted for free.

## Netlify (sabse aasaan, 1 minute)
1. https://app.netlify.com/drop kholo (free account se login).
2. Is `risk-calculator` folder ko (ya `risk-calculator.zip` ko unzip karke folder ko) drag & drop karo.
3. Site settings > Change site name > jaise `tradingwizaard-risk` → link: https://tradingwizaard-risk.netlify.app

## Vercel
1. https://vercel.com > Add New > Project > Import Git repo `harshkt214/material-theme`.
2. Root Directory = `tools/risk-calculator`, Framework Preset = Other, Build command khaali.
3. Deploy.

## Kya karta hai
- Equity mode: Capital × Risk% = max risk; max risk ÷ |Entry − SL| = shares (neeche round).
- F&O mode: quantity ÷ lot size = lots (neeche round). Presets: NIFTY 65, BANKNIFTY 30, FINNIFTY 60, MIDCPNIFTY 120, SENSEX 20. Lot sizes exchange badalta hai, deploy se pehle check karke `<select id="inst">` ke values update karo.
- Optional target → Risk:Reward aur break-even win rate.
- Warnings: 1 lot bhi fit na ho, position value > capital, risk > 2%.
