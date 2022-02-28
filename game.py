import os
import matplotlib.pyplot as plt
from agents import * 
from datetime import datetime
# Number of agents participating
agent_number = 1000



dirpath =os.path.dirname(__file__)+"/Game_Runs"
print(sum(prob))
# helper function:
def _helper(input: Agent) -> int:
    return input.choose()
# Stuff related to setting up the output
time_curr = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')


# Generate agents with the prob from agents.py (this becomes an array of agents)
b = AgentGenerator.generate_agents_prob(prob, agent_number)

# The array of the each agent's guess
guesses= np.vectorize(_helper)(b)

# find unique guesses
unique, counts = np.unique(guesses, return_counts=True)

# find winning value (closes to 2/3 of average)
winning_value =guesses[(np.abs(guesses - round(2*np.average(guesses)/3))).argmin()]
list_of_winners = []

# Make dir to save our files
os.mkdir(dirpath+"/"+time_curr)

# Information about current run:
winning_string="Run with probabiliies of %s. Yielding correct guess of %d. Total number of agents: %d\n" % (prob, winning_value, agent_number)
for agent in b:
    if agent.choice == winning_value:
        list_of_winners.append( type(agent).__name__)
        winning_string+=agent.__str__()
        winning_string+="\n"
with open(dirpath+"/"+time_curr+'/winners.txt', 'w') as f:
    f.write(winning_string)
print(winning_string)

# Show and save plots:
plt.figure(figsize=(18, 8))
plt.bar(unique, counts, width=0.6, align='edge')
plt.xticks(unique, fontsize = 8)
plt.margins(0)
plt.savefig(dirpath+"/"+time_curr+"/plt1.png", dpi=100)
plt.show()

# Show the winners (and save the plot):
unique, counts = np.unique(list_of_winners, return_counts=True)

plt.figure(figsize=(18, 8))
plt.bar(unique, counts, width=0.6, align='edge')
plt.xticks(unique, fontsize = 8)
plt.yticks(np.arange(0,100))
plt.margins(0)
plt.savefig(dirpath+"/"+time_curr+"/plt2.png", dpi=100)
plt.show()

print(counts)
print(winning_value)
