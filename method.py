from DATA import Data

def WeightRank(data):
	return sorted(data.OutweightDic, key=lambda x: data.OutweightDic[x], reverse=True)

def PageRank(data):
	N = len(data.threshold)
	turn = 1
	score = {}
	tmp_score = {}
	for x in range(1, N+1):
		score[str(x)] = 1.0
		tmp_score[str(x)] = 1.0
	SumOfScore = sum(score.values())
	while turn < 3:
		for node in data.threshold.keys():
			tmp = 0
			if node not in data.OutdegreeDic.keys(): continue
			for outd in data.OutdegreeDic[node]:
				tmp += score[outd[0]] / len(data.IndegreeDic[outd[0]])
			tmp_score[node] = tmp
		score = dict(tmp_score)
		if sum(score.values()) == SumOfScore:
			turn += 1
		else:
			SumOfScore = sum(score.values())
			turn = 1
	return sorted(score, key=lambda x: score[x], reverse=True)

def diffusion(seed, data, active, inactive):
	active.append(seed)
	inactive.remove(seed)
	numberOfActive = len(active)
	turn = 0
	tmp_active = list(active)
	tmp_inactive = list(inactive)
	while turn < 3:
		for node in inactive:
			if node not in data.IndegreeDic.keys(): continue
			cntInfluence = 0
			for n in data.IndegreeDic[node]:
				if n[0] in active:
					cntInfluence += n[1]
			if data.threshold[node] <= cntInfluence:
				tmp_active.append(node)
				tmp_inactive.remove(node)
		active = list(tmp_active)
		inactive = list(tmp_inactive)
		if numberOfActive == len(active):
			turn += 1
		else:
			numberOfActive = len(active)
			turn = 1
	return numberOfActive


def Greedy(data, active, inactive):
	SEED = ''
	maxSpread = 0
	for seed in inactive:
		tmp = diffusion(seed, data, list(active), list(inactive)) - len(active)
		if tmp > maxSpread:
			maxSpread = tmp
			SEED = seed
		print("seed:", seed)
		print(tmp)
	return SEED

def MaxWeight(data, inactive, weight_rank):
	if not weight_rank: WeightRank(data)
	for r in weight_rank:
		if r in inactive:
			return r

def MaxPageRank(data, inactive, page_rank):
	if not page_rank: PageRank(data)
	for r in page_rank:
		if r in inactive:
			return r

def FindCandidate(data, your_active, inactive):
	candidate = []
	for node in your_active:
		if node not in data.OutdegreeDic.keys(): continue
		for outd in data.OutdegreeDic[node]:
			if outd[0] not in inactive or outd[0] not in data.IndegreeDic.keys(): continue
			for ind_L1 in data.IndegreeDic[outd[0]]:
				if ind_L1[0] not in inactive or ind_L1[0] not in data.IndegreeDic.keys(): continue
				for ind_L2 in data.IndegreeDic[ind_L1[0]]:
					if ind_L2[0] not in inactive: continue
					candidate.append(ind_L2[0])
	return candidate


def CMaxWeight(data, your_active, inactive, weight_rank):
	if not weight_rank: WeightRank(data)
	if not your_active: return MaxWeight(data, inactive)
	candidate = FindCandidate(data, your_active, inactive)
	for r in weight_rank:
		if r in candidate:
			return r


def CMaxPageRank(data, your_active, inactive, page_rank):
	if not page_rank: PageRank(data)
	if not your_active: return MaxWeight(data, inactive)
	candidate = FindCandidate(data, your_active, inactive)
	for r in page_rank:
		if r in candidate:
			return r

def CSelection(data, active, your_active, inactive, weight_rank):
	if not weight_rank: WeightRank(data)
	if not your_active: return MaxWeight(data, inactive)
	diff = dict(data.threshold)
	for node in diff.keys():
		power = 0
		if node not in data.IndegreeDic.keys(): continue
		for w in data.IndegreeDic[node]:
			if w[0] in active:
				diff[node] -= w[1]
	candidate = FindCandidate(data, your_active, inactive)
	got = {}
	for c in candidate:
		got[c] = 0
		if c not in data.OutdegreeDic.keys(): continue
		for n_L1 in data.OutdegreeDic[c]:
			if n_L1[1] >= diff[n_L1[0]]:
				if n_L1[0] not in data.OutdegreeDic.keys(): continue
				for n_L2 in data.OutdegreeDic[n_L1[0]]:
					if n_L2[1] >= diff[n_L2[0]]:
						got[c] += 1
	rank = sorted(got, key=lambda x: got[x], reverse=True)
	for x in range(len(rank)-1):
		if rank[x] > rank[x+1]:
			return rank[x]
		else:
			if weight_rank.index(rank[x]) < weight_rank.index(rank[x+1]):
				return rank[x]
			else:
				return rank[x+1]
	

def Voting(data, active, your_active, inactive, weight_rank, page_rank):
	vote = {}
	SEED = []
	#SEED.append(Greedy(data, active, inactive))
	SEED.append(MaxWeight(data, inactive, weight_rank))
	SEED.append(MaxPageRank(data, inactive, page_rank))
	SEED.append(CMaxWeight(data, your_active, inactive, weight_rank))
	SEED.append(CMaxPageRank(data, your_active, inactive, page_rank))
	SEED.append(CSelection(data, active, your_active, inactive, weight_rank))
	print(SEED)
	if len(set(SEED)) == len(SEED):
		return SEED[0]
	else:
		for s in SEED:
			if s not in vote.keys():
				vote[s] = 1
			else:
				vote[s] += 1
		return sorted(vote, key=lambda x: vote[x], reverse=True)[0]

	
