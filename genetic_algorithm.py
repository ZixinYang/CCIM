import setting
from random import (choice, random, randint)
from LT_diffusion import Spreading

class Chromosome:
	def __init__(self, gene, fitness=0, active=None, my_active=None, your_active=None, inactive=None):
		self.gene = gene
		self.fitness = fitness
		self.active = active
		self.my_active = my_active
		self.your_active = your_active
		self.inactive = inactive
	def gen_mate()
	def mate(self, mate, active, my_active, your_active, inactive):
		pivot = randint(0, len(self.gene)-1)
		gene1 = list(self.gene)
		gene2 = list(mate.gene)
		pivot_value = gene1[pivot]
		gene1[pivot] = gene2[pivot]
		gene2[pivot] = pivot_value
		update1 = Chromosome._update_active_state(gene1, active, my_active, your_active, inactive)
		update2 = Chromosome._update_active_state(gene2, active, my_active, your_active, inactive)
		return Chromosome(gene1, update1[0], update1[1], update1[2], update1[3], update1[4]), Chromosome(gene2, update2[0], update2[1], update2[2], update2[3], update2[4])
	
	def mutate(self, active, my_active, your_active, inactive):
		gene = list(self.gene)
		tmp_active = list(active)
		tmp_inactive = list(inactive)
		for g in gene:
			tmp_active.append(g)
			if g not in tmp_inactive:
				print("g is not in tmp_inactive, g: ", g)
				print(len(tmp_inactive))
				continue
			tmp_inactive.remove(g)
		potential = choice(tmp_inactive)
		idx = randint(0, len(gene) - 1)
		gene[idx] = potential
		update = Chromosome._update_active_state(gene, active, my_active, your_active, inactive)
		return Chromosome(gene, update[0], update[1], update[2], update[3], update[4])
	
	@staticmethod
	def _update_fitness(my_active, your_active):
		return len(my_active) * (len(my_active) + len(your_active))
		
	@staticmethod
	def gen_random(active, my_active, your_active, inactive, left_turns):
		gen_seed = []
		for x in range(left_turns*2):
			seed = choice(inactive)
			print("Random seed: %s"%(seed))
			gen_seed.append(seed)
			active.append(seed)
			inactive.remove(seed)
			if x%2 == 0:
				my_active.append(seed)
			else:
				your_active.append(seed)
			cnt = Spreading(list(active), list(my_active), list(your_active), list(inactive))
			active = list(cnt[0])
			my_active = list(cnt[1])
			your_active = list(cnt[2])
			inactive = list(cnt[3])
		return Chromosome(gen_seed, Chromosome._update_fitness(my_active, your_active), list(active), list(my_active), list(your_active), list(inactive))
	
	@staticmethod
	def _update_active_state(gene, active, my_active, your_active, inactive):
		tmp_active = list(active)
		tmp_my_active = list(my_active)
		tmp_your_active = list(your_active)
		tmp_inactive = list(inactive)
		for i in range(len(gene)):
			if gene[i] in tmp_active: continue
			tmp_active.append(gene[i])
			tmp_inactive.remove(gene[i])
			if i%2==0:
				tmp_my_active.append(gene[i])
			else:
				tmp_your_active.append(gene[i])
			cnt = Spreading(list(tmp_active), list(tmp_my_active), list(tmp_your_active), list(tmp_inactive))
			tmp_active = list(cnt[0])
			tmp_my_active = list(cnt[1])
			tmp_your_active = list(cnt[2])
			tmp_inactive = list(cnt[3])
		
		return [Chromosome._update_fitness(my_active, your_active), tmp_active, tmp_my_active, tmp_your_active, tmp_inactive]
		
class Population:

	_tournamentSize = 3

	def __init__(self, size=1024, crossover=0.8, elitism=0.01, mutation=0.03, active=None, my_active=None, your_active=None, inactive=None, left_turns=10):
		self.elitism = elitism
		self.crossover = crossover
		self.mutation = mutation
		self.active = list(active)
		self.my_active = list(my_active)
		self.your_active = list(your_active)
		self.inactive = list(inactive)

		buf = []
		for i in range(size): buf.append(Chromosome.gen_random(list(self.active), list(self.my_active), list(self.your_active), list(self.inactive), left_turns))
		self.population = list(sorted(buf, key=lambda x: x.fitness, reverse=True))

	def _tournament_selection(self):
		best = choice(self.population)
		for i in range(Population._tournamentSize):
			cont = choice(self.population)
			if cont.fitness < best.fitness: best = cont

		return best

	def _selectParents(self):
		return (self._tournament_selection(), self._tournament_selection())

	def evolve(self):
		size = len(self.population)
		idx = int(round(size*self.elitism))
		buf = self.population[:idx]
		while idx < size:
			if random() <= self.crossover:
				(p1, p2) = self._selectParents()
				while p1.gene == p2.gene:
					(p1, p2) = self._selectParents()
				children = p1.mate(p2, list(self.active), list(self.my_active), list(self.your_active), list(self.inactive))
				for c in children:
					if random() <= self.mutation:
						buf.append(c.mutate(list(self.active), list(self.my_active), list(self.your_active), list(self.inactive)))
					else:
						buf.append(c)
				idx += 2
			else:
				if random() <= self.mutation:
					buf.append(self.population[idx].mutate(list(self.active), list(self.my_active), list(self.your_active), list(self.inactive)))
				else:
					buf.append(self.population[idx])
				idx += 1
		self.population = list(sorted(buf[:size], key=lambda x: x.fitness, reverse=True))


def GA(active, my_active, your_active, inactive, left_turns):
	#maxGeneration = 200
	pop = Population(50, 0.8, 0.5, 0.03, active, my_active, your_active, inactive, left_turns)
	#for i in range(1, maxGeneration + 1):
	max_fitness = 0
	TURN = 0
	while TURN < 20:
		print("Generation: {0}\nGene: {1}\nFitness: {2}\nActive state: my: {3}, your: {4}".format(TURN+1, pop.population[0].gene, pop.population[0].fitness, len(pop.population[0].my_active), len(pop.population[0].your_active)))
		pop.evolve()
		tmp_fitness = pop.population[0].fitness + pop.population[1].fitness + pop.population[2].fitness + pop.population[3].fitness + pop.population[4].fitness
		if max_fitness == tmp_fitness:
			TURN += 1
		else:
			TURN = 0
			if tmp_fitness > max_fitness:
				max_fitness = tmp_fitness
	print("Gene: {0}\nFitness: {1}\nActive state: my: {2}, your: {3}".format(pop.population[0].gene, pop.population[0].fitness, len(pop.population[0].my_active), len(pop.population[0].your_active)))
	print("Gene: {0}\nFitness: {1}\nActive state: my: {2}, your: {3}".format(pop.population[1].gene, pop.population[1].fitness, len(pop.population[1].my_active), len(pop.population[1].your_active)))
	print("Gene: {0}\nFitness: {1}\nActive state: my: {2}, your: {3}".format(pop.population[2].gene, pop.population[2].fitness, len(pop.population[2].my_active), len(pop.population[2].your_active)))
	print("Gene: {0}\nFitness: {1}\nActive state: my: {2}, your: {3}".format(pop.population[3].gene, pop.population[3].fitness, len(pop.population[3].my_active), len(pop.population[3].your_active)))
	print("Gene: {0}\nFitness: {1}\nActive state: my: {2}, your: {3}".format(pop.population[4].gene, pop.population[4].fitness, len(pop.population[4].my_active), len(pop.population[4].your_active)))

	return


