from readData import readFile
from method import WeightRank
from method import PageRank

data = readFile()
weight_rank = WeightRank(data)
page_rank = PageRank(data)
