import pandas as pd
import os
from datetime import datetime
class Data(object):
	def __init__(self):
		pass
	def get_data_frame(self, sym, start, end):
		path="."
		df=pd.read_csv(os.path.join(path,sym+".BK.csv"), index_col=0)
		return df[(start.strftime("%Y-%m-%d")<df.index)&(df.index<=end.strftime("%Y-%m-%d"))].copy()
