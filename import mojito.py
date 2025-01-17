import mojito
import pprint
import pandas as pd
from datetime import date, time, datetime


key = "PSEzmlJNXm7W1nGGuZZsXug6IYR75Jj7KuC1"
secret = "djTwejt5iK+dXikl0Ilp+hE94ztGE11kUUp0xMTklVdgRJQkF/F2kwVoXOZnKI14Pv0OtSHQCWxQ543aD32RnuJXo4dgS9JIOQUj1AZHzNUqurIckjR/dawghxNNYnftf8/rh3yU+AjxMOoah9eNa/TmHCjmAFL/qKRs1nGd7M0XnJLK7vQ="
acc_no = "50085747-01"

broker = mojito.KoreaInvestment(
    api_key=key,
    api_secret=secret,
    acc_no=acc_no,
    mock=True
)


#잔고 가져오기
balance = int(broker.fetch_balance()['output2'][0]['dnca_tot_amt'])


#Band 갭 조정
P_band = 0.005  
D_band = 0.04

#P_Inverse2X : Kodex 코스피 인버스 2X
#P_Leverage : Kodex 코스피 레버리지

KODEX_KOSPI200_INVERSE2X = '252670'
KODEX_KOSPI200_LEVERAGE = '122630'

P_Inverse2X = broker.fetch_ohlcv(
    symbol=KODEX_KOSPI200_INVERSE2X,
    timeframe='D',
    adj_price=True
)

P_Leverage  = broker.fetch_ohlcv(
    symbol=KODEX_KOSPI200_LEVERAGE,
    timeframe='D',
    adj_price=True
)


PI_close = int(P_Inverse2X['output1']['stck_prdy_clpr'])
PL_close = int(P_Leverage['output1']['stck_prdy_clpr'])

PI_price = int(P_Inverse2X['output1']['stck_prpr'])
PL_price = int(P_Leverage['output1']['stck_prpr'])

PI_cap = PI_close * (1 + P_band)
PL_cap = PL_close * (1 + P_band)

PI_loss = PI_close * (1 - P_band)
PL_loss = PL_close * (1 - P_band)

today = datetime.today()
hour = int(str(today.hour)) + 9
minute = int(str(today.minute))

time = hour * 60 + minute

#주가 호가단위에 맞춰서 바꾸기
def Round(price):
    tick1 = 5  #주가 2000 ~ 5000
    tick2 = 10 #주가 5000 ~ 20000   
    tick3 = 50 #주가 20000 ~ 50000  
    if price < 5000 and price % tick1 != 0:
        price += tick1 - (price % tick1)
    elif price < 20000 and price % tick2 != 0:
        price += tick2 - (price % tick2)
    elif price % tick3 != 0:
        price += tick3 - (price % tick3)

    return price



#Kodex Inverse 2X 매수가 설정
PI_cap = Round(PI_cap)

#Kodex Inverse 2X 매도가 설정
PI_loss = Round(PI_loss)

#Kodex Leverage 매수가 설정
PL_cap = Round(PL_cap)

    
#Kodex Leverage 매도가 설정
PL_loss = Round(PL_loss)

#매매 state 변수 설정
if_buy_ins = 0
if_buy_lv = 0


while 539 <= time < 900:
    P_Inverse2X = broker.fetch_ohlcv(
        symbol="252670",
        timeframe='D',
        adj_price=True
    )

    P_Leverage  = broker.fetch_ohlcv(
        symbol="122630",
        timeframe='D',
        adj_price=True
    )

    PI_price = int(P_Inverse2X['output1']['stck_prpr'])
    PL_price = int(P_Leverage['output1']['stck_prpr'])


    if PI_price >= PI_cap and if_buy_ins == 0:

        #Kodex Inverse 2X 매수
        PI_buy = broker.create_limit_buy_order(
            symbol="252670",
            price=str(int(PI_cap)),
            quantity=str(int(balance // PI_cap))
        )

        if_buy_ins += 1


    if PL_price >= PL_cap and if_buy_lv == 0:

        #Kodex Leverage 매수
        PL_buy = broker.create_limit_buy_order(
            symbol="122630",
            price=str(int(PL_cap)),
            quantity=str(int(balance // PL_cap))
        )

        if_buy_lv += 1

    if broker.fetch_balance()['output1']:

        #Kodex Inverse 2X 매도
        PI_sell = broker.create_limit_sell_order(
            symbol="252670",
            price=str(int(PI_loss)),
            quantity=str(int(broker.fetch_balance()['output1'][0]['hldg_qty']))
        )

        #Kodex Leverage 매도
        PL_sell = broker.create_limit_sell_order(
            symbol="122630",
            price=str(int(PL_loss)),
            quantity=str(int(broker.fetch_balance()['output1'][0]['hldg_qty']))
        )
        print('a')
    
    print(('b'))
    

while 900 <= time:
    #Kodex Inverse 2X 매도
    PI_sell = broker.create_market_sell_order(
        symbol="252670",
        quantity=str(int(broker.fetch_balance()['output1'][0]['hldg_qty']))
    )

    #Kodex Leverage 매도
    PL_sell = broker.create_market_sell_order(
        symbol="122630",
        quantity=str(int(broker.fetch_balance()['output1'][0]['hldg_qty']))
    )    





    # if broker.fetch_balance()['output1']['prdt_name'] == 'KODEX 레버리지':

    #     #Kodex Leverage 매도 
    #     PL_sell = broker.create_limit_sell_order(
    #         symbol="122630",
    #         price=str(int(PL_loss)),
    #         quantity=str(int(balance // PL_loss))
    #     )



# print(PI_loss)
# print(P_Inverse2X['output1']['stck_prdy_clpr'])


# 개장동안 loop
# while 540 <= time <= 930:
#     PI_price = broker.fetch_price("252670")['output']['stck_prpr']










# 코스피 곱버스 df
# Inverse2X = broker.fetch_ohlcv(
#     symbol="252670",
#     timeframe='d',
#     adj_price=True
# )
#
# IVX = pd.DataFrame(Inverse2X['output2'])
# dt = pd.to_datetime(IVX['stck_bsop_date'], format="%Y%m%d")
# IVX.set_index(dt, inplace=True)
# IVX = IVX[['stck_oprc', 'stck_hgpr', 'stck_lwpr', 'stck_clpr']]
# IVX.columns = ['open', 'high', 'low', 'close']
# IVX.index.name = "date"
# print(IVX)

# 코스피 레버리지 df
# Leverage = broker.fetch_ohlcv(
#     symbol="122630",
#     timeframe='W',
#     adj_price=True
# )
# 
# LVG = pd.DataFrame(Leverage['output2'])
# dt = pd.to_datetime(LVG['stck_bsop_date'], format="%Y%m%d")
# LVG.set_index(dt, inplace=True)
# LVG = LVG[['stck_oprc', 'stck_hgpr', 'stck_lwpr', 'stck_clpr']]
# LVG.columns = ['open', 'high', 'low', 'close']
# LVG.index.name = "date"



