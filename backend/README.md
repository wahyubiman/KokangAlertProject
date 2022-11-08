## Crypto MSB alert project

## app that send alert the discord when Market Structure Break happen on specific timeframe

---

Requirement

- python
- nodejs

Install

```bash
# Clone repo
git clone https://github.com/WahyuBiman/KokangAlertProject.git
cd KokangAlertProject

# make python virtual environment using virtualnenv
virtualenv name
source name/bin/activate

# install pm2
npm install pm2 -g

# run
cd backend
pm2 start main.py

```

---

### TODO

- Add Frontend:
  > - add position size calculator
  > - crypto dashboard
  > - trend based on MSB in 1h, 4h, 1d timeframe
  > - add RSI breakout alert
- Add Backend:
  > - Add spot MSB scanner
  > - Add Trendline Breakout alert
  > - Add RSI Breakout Trendline alert
