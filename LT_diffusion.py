import setting

def Spreading(active, my_active, your_active, inactive):
	tmp_active = list(active)
	tmp_inactive = list(inactive)
	tmp_my_active = list(my_active)
	tmp_your_active = list(your_active)
	numberOfActive = len(tmp_active)
	turn = 1
	while turn < 3:
		for node in inactive:
			if node not in setting.data.IndegreeDic.keys(): continue
			total_weight = 0
			my_weight = 0
			your_weight = 0
			for ind in setting.data.IndegreeDic[node]:
				if ind[0] in tmp_my_active:
					total_weight += ind[1]
					my_weight += ind[1]
				elif ind[0] in tmp_your_active:
					total_weight += ind[1]
					your_weight += ind[1]
			if total_weight >= setting.data.threshold[node]:
				tmp_active.append(node)
				tmp_inactive.remove(node)
				if my_weight >= your_weight:
					tmp_my_active.append(node)
				else:
					tmp_your_active.append(node)
		if len(tmp_active) == numberOfActive:
			turn += 1
		else:
			numberOfActive = len(tmp_active)
			turn = 1
		active = list(tmp_active)
		inactive = list(tmp_inactive)
		my_active = list(tmp_my_active)
		your_active = list(tmp_your_active)

	return [active, my_active, your_active, inactive]
