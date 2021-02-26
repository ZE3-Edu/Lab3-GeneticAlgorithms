###############################################
### CMPLXSYS425 - Evolution in silico       ###
### Lab 3 -- ROAD TRIP!                     ###
### ####################################### ###

import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy


### ####################################### ###
#### First, let's figure out what the location data is going to look like. ####
# We know we want a list of the destinations
road_trip_destinations = []

# And we could use a dictionary, which if you're not familiar with yet 
# definitely check them out, to store the name and location of each spot.
# https://docs.python.org/3/tutorial/datastructures.html#dictionaries
ann_arbor = dict(name="Ann Arbor", location=(0,0))
other_spot = dict(name="Chicago", location=(-250, -20))

# to simplify things, let's just use x,y coordinates for locations, and call
# Ann Arbor the center of the universe. The () around 0,0 creates another
# common data structure in python, a tuple. 
print(ann_arbor, other_spot)

# now we can ask for different values by name (i.e., key)
print(ann_arbor['location'])

# Let's get a little help calculating distances between locations from
# SciPy's distance module. 
from scipy.spatial import distance

# Fortunately, this function already expects our x,y[,z,t,...] coordinates
# in pairs. What a lucky choice we made :).
aa_to_chi = distance.euclidean(ann_arbor['location'], other_spot['location'])
print(aa_to_chi)



### ####################################### ###
#### Next, we need to code up the individuals in our genetic algorithm #####

# Our individuals aren't just 0s and 1s anymore, so let's create a "class" 
# that holds their data, and can even do some of the work of 
# mutations/crossover for us!

# We know each individual is going to include each location, just in different
# orders, so we can just randomly permute the locations in our first pass!

class Individual:
    #Just a little python background:
    #Classes in python call the __init__ function when you create new 
    #instances. They hold a reference to their own object (self) that
    #gets passed to every method.
    def __init__(self, location_data):
        #let's hold on to the location data, and just the names too
        #deepcopy so we don't end up changing it on accident! 
        self.location_data = deepcopy(location_data)
        self.genome = np.random.permutation(self.location_data)
    
    def evaluate(self):
        # We need to calculate the "fitness" of this organism, which is based 
        # on traveling the entire trip and returning back to the first spot
        tot_dist = 0
        
        # This is a little Python trick to calculate that last link back to
        # our starting point, we'll start at `-1`, which loops around to the 
        # last item in our list! 
        for i in range(-1, len(self.genome)-1):
            tot_dist += distance.euclidean( self.genome[i]['location'],
                                            self.genome[i+1]['location'])

        # One problem you may have noticed is that we're trying to find
        # the *MINIMUM* distance, so we need to translate large distances 
        # into low fitnesses. Here's one (not great) way.
        fitness = 1/tot_dist

        return fitness

    def mutate(self):
        # This is not a good mutation function, so you should probably
        # ditch it and write your own!
        self.genome = np.random.permutation(self.genome)

    def get_offspring(self):
        # return a copy of this organism!
        new_individual = Individual(self.location_data)
        new_individual.genome = deepcopy(self.genome)
        return new_individual

# Play with this a little bit to get a feel for what's going on!
a = Individual([ann_arbor, other_spot])
b = a.get_offspring()
print(b)



### ####################################### ###
#### Now we have individuals, and fitnesses, let's make a population! #####

# You might consider cleaning this up into a Population class...
# But, we also need to make some locations... let's do this randomly for now
locations = []
num_locations = 50

for i in range(num_locations):
    loc_x = np.random.uniform(low=-2500, high=900)
    loc_y = np.random.uniform(low=-1300, high=600)
    locations.append( dict(name=i, location=(loc_x, loc_y)) )

# Not the most interesting spots to visit, but they'll do
print(locations)

pop_size = 100
num_generations = 100
mut_rate = 0.05 #5%

# Build our population
population = [Individual(locations) for _ in range(pop_size)]

# We can measure the fitness of each individual in our population
# Then normalize it to sum to 1...
fitnesses = [org.evaluate() for org in population]
norm_fitness = fitnesses/np.sum(fitnesses)
print(norm_fitness, np.sum(norm_fitness))

# And now, we need a way to do selection... 
# -- recall the np.random.choice() function you all are experts on now
to_reproduce = np.random.choice(population, replace=True, size=pop_size, p=norm_fitness)

# Whoa, we did the whole selection step in a single line!
# What kind of selection method is this? Think about how an individual's fitness
# affects it's probability of being selected... You'll probably want to change
# this selection mechanism, too! 

# Let's actually create the next generation now with mutations and everything!
new_population = []
for chosen_org in to_reproduce:
    new_org = chosen_org.get_offspring()
    if np.random.rand() < mut_rate:
        new_org.mutate()

    new_population.append(new_org)

print(new_population)

# Well, that's cool but we need to do this over and over, so let's put this
# whole thing together now. 

# We'll keep using Python Object Oriented Programing for this...
class Population:
    def __init__(self, pop_size, mut_rate, location_data):
        self.pop_size = pop_size
        self.mut_rate = mut_rate
        self.location_data = location_data
        #same old population code, with some extra "self"s
        self.population = [Individual(self.location_data) for _ in range(self.pop_size)]

    def get_absolute_fitnesses(self):
        return [org.evaluate() for org in self.population]

    def get_normalized_fitnesses(self):
        fitnesses = self.get_absolute_fitnesses()
        return fitnesses/np.sum(fitnesses)
    
    def step_generation(self):
        #Selection (You'll want to make this better!)
        to_reproduce = np.random.choice(self.population, replace=True, size=self.pop_size, p=self.get_normalized_fitnesses())

        new_population = []
        for chosen_org in to_reproduce:
            #Reproduction (Add Recombination??)
            new_org = chosen_org.get_offspring()
            if np.random.rand() < self.mut_rate:
                #Mutation (Another place to improve!)
                new_org.mutate()

            new_population.append(new_org)
        self.population = new_population

# Now let's use our nice OO (object-oriented) population!
# Notice I'm passing in values for the pop_size and mut_rate instead of using
# our variables -- just to show you that you can!
p = Population(pop_size=100, mut_rate=0.05, location_data=locations)

num_generations = 50
average_fitnesses = [ np.mean(p.get_absolute_fitnesses()) ]

# Note, this does take a bit of time to run! If you want to speed it up,
# go for it! Changing your representation could have a very big effect! 
for t in range(num_generations):
    print("Generation {0}".format(t))
    #Step the population forward one generation
    p.step_generation()
    #Keep track of the average fitness
    average_fitnesses.append(np.mean(p.get_absolute_fitnesses()))

plt.plot(average_fitnesses)
plt.ylabel("Fitness (1/distance")
plt.xlabel("Generation")
plt.show()
