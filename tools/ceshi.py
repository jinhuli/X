from WindPy import *
import pandas as pd

w.start()

data = w.wss("300011.SZ,300015.SZ,300018.SZ", "mkt_freeshares,pre_close","unit=1;tradeDate=20181018;priceAdj=U;cycle=D")
target_po =pd.DataFrame(data.Data, columns=data.Codes, index=data.Fields).T
sum = target_po["MKT_FREESHARES"].sum()
margin = 0.8
vl = query_capital().get_field("total_asset")[0]*margin
target_po["weight"] = [i/sum for i in  target_po["MKT_FREESHARES"].tolist()]
target_po["target_vl"] = [i*vl for i in  target_po["weight"].tolist()]

now_position = query_position().get_dataframe()

