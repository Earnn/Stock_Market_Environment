import pandas as pd
import os, json
from datetime import datetime
class Env(object):
	def __init__(self,_sym,cash,range_day):
		self.sym = _sym
		self.range_day = range_day
		self.cash = cash
		self.capital_gain = 0
		self.end=datetime(2017,9,17)
		start=datetime(1970,9,17)
		self.df=get_data_frame(_sym,start,self.end)
		self.day = 0
		self.principle = 0
		self.volume = 0
		self.equity = 0
		self.reward = 0
		self.observation = []
		self.observation.append(self.cash)
		self.observation.append(self.equity)
		self.observation.append(self.capital_gain)		
		for i in range(self.range_day) :
			if i < self.range_day-1:
				current_price = ((self.df['High'][self.day] + self.df['Low'][self.day])/2)
				next_current_price = ((self.df['High'][self.day+1] + self.df['Low'][self.day+1])/2)
				percent = (next_current_price - current_price)/current_price 
				self.observation.append(percent)

			# current_price = ((self.df['High'][self.day] + self.df['Low'][self.day])/2)
			self.day +=1



		print(self.df)

	def reset(self):
		self.sym = _sym
		self.cash = 10000
		self.capital_gain = 0
		self.end=datetime(2017,9,17)
		start=datetime(1970,9,17)
		self.df=get_data_frame(_sym,start,self.end)
		self.day = 0
		self.principle = 0
		self.volume = 0
		self.equity = 0
		self.reward = 0
		self.observation = []
		self.observation.append(self.cash)
		self.observation.append(self.equity)
		self.observation.append(self.capital_gain)		
		for i in range(30) :
			if i < 29:
				current_price = ((self.df['High'][self.day] + self.df['Low'][self.day])/2)
				next_current_price = ((self.df['High'][self.day+1] + self.df['Low'][self.day+1])/2)
				percent = (next_current_price - current_price)/current_price 
				self.observation.append(percent)

			# current_price = ((self.df['High'][self.day] + self.df['Low'][self.day])/2)
			self.day +=1

	def step(self, action):
		
		if action == 0:
			info = "BUY"
			current_price = ((self.df['High'][self.day] + self.df['Low'][self.day])/2)*100
			if(current_price <= self.cash ):
				# self.principle = price
				self.equity = self.volume*current_price #equuty is มุลค่าทั้งหมดของหุ้นตอนนั้น
				self.volume += 100
				self.cash = self.cash - current_price
				self.day+=1
				capital_gain_previous = self.capital_gain
				self.capital_gain = self.cash + self.equity
				

				# observation.append()
				if self.day == 30:
					self.reward  =  0
				else:
					self.reward +=  self.capital_gain - capital_gain_previous 
					# pass


				if( self.day == len(self.df) ):
					return self.observation,self.reward,True,("End date")

				return  self.observation,self.reward,False,("Bid %f. Total cash is %f. Volume is %f. Capital_gain %f "%(current_price,self.cash,self.volume,self.capital_gain))
			else :
				return  self.observation,self.reward,False,'Not enough cash'



		elif action == 1:
			self.day+=1
			if(self.day == len(self.df)):
					return self.observation,self.reward,True,("End date")
			return(self.observation,self.reward,False,'Do nothing')
			
		elif action == 2:

			current_price = ((self.df['High'][self.day] + self.df['Low'][self.day])/2)*100
			# print("sell ",sell)
			# print("df ",self.df['High'][self.day])
			# print("principle ",self.principle)
			self.cash =  self.volume* current_price
			self.day+=1
			capital_gain_previous = self.capital_gain
			self.capital_gain = self.cash + (self.volume*current_price)
			self.volume += 100
			if self.volume > 0:
				self.reward +=  self.capital_gain - capital_gain_previous 
			
			
			
			self.volume =0
			self.equity = self.volume*current_price #equuty is มุลค่าทั้งหมดของหุ้นตอนนั้น		

			if(self.day == len(self.df) ):
				return self.observation,self.reward,True,("End date")
			return self.observation,self.reward,False,('Sell %f . Total cash is %f. Capital gain is %f'%(current_price,self.cash,self.capital_gain))

		else :
			pass

			

		# observation=None
		# reward=None
		# done=None
		# info=None
		
	def render(self):
		return ("Total cash is %f. Capital gain is %f. Equity is %f. Current price is %f. "%(self.cash,self.capital_gain,self.equity,(self.cash+self.equity)))
	def state_len(self):
		return len(self.observation)
	def action_space(self):
		return 3


def get_data_frame(sym, start, end):
	#to_datetime = lambda d: datetime.strptime(d, "%Y-%m-%d")
	path, filename = os.path.split(os.path.abspath(__file__))
	df=pd.read_csv(os.path.join(path,sym+".BK.csv"), index_col=[0],converters={'Date': pd.to_datetime})
	return df[(start.strftime("%Y-%m-%d")<df.index)&(df.index<=end.strftime("%Y-%m-%d"))].copy()

def get_symbol_key():
	path, filename = os.path.split(os.path.abspath(__file__))
	return json.load( open(os.path.join(path,"sym_key.json"),"r"))
def get_set_list():
	path, filename = os.path.split(os.path.abspath(__file__))
	out=[]
	for i in json.load( open(os.path.join(path,"set_list.json"),"r")):
		out.append(i.split('.')[0])
	return out
def new_columns(sym):
	return {

		'Open': sym+'_Open', 
		'High': sym+'_High',
		'Low':sym+'_Low',
		'Close':sym+'_Close',
		'Adj Close': sym,
		'Volume':sym+'_Volume'
		}
def get_adj(sym_list, start, end):
	sym=sym_list[0]
	df1=get_data_frame(sym,start,end)
	df1.rename(columns=new_columns(sym), inplace=True)
	#print(df1)
	df1 = df1[[df1.columns[4]]]
	for sym in sym_list[1:]:
		df2=get_data_frame(sym,start,end)
		df2.rename(columns=new_columns(sym), inplace=True)
		df2 = df2[[df2.columns[4]]]
		df1=pd.merge(df1,df2,how='outer',left_index=True, right_index=True)
	return df1.copy()

