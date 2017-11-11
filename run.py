import setting

from method import Greedy
from method import MaxWeight
from method import MaxPageRank
from method import CMaxWeight
from method import CSelection
from method import Voting
from LT_diffusion import Spreading
from genetic_algorithm import GA
from readData import readFile

#Greedy(data, active, inactive)
#MaxWeight(data, inactive, weight_rank)
#MaxPageRank(data, inactive, page_rank)
#CMaxWeight(data, your_active, inactive, weight_rank)
#CMaxPageRank(data, your_active, inactive, page_rank)
#CSelection(data, active, your_active, inactive, weight_rank)

if __name__ == "__main__":
	#weight_rank = WeightRank(data)
	#page_rank = PageRank(data)
	Active = []
	my_Active = []
	your_Active = []
	Inactive = [str(a) for a in range(1, 6302)]
	#Inactive.remove('23')
	#Inactive.remove('33')
	#print(data.OutdegreeDic['23'])
	#print(data.OutdegreeDic['33'])
	#print(Greedy(data, Active, Inactive))
	#print(Voting(data, active, your_active, inactive, weight_rank, page_rank))
	#print(len(Spreading(data, Active, my_Active, your_Active, Inactive)[2]))
	print(GA(Active, my_Active, your_Active, Inactive, 10))
