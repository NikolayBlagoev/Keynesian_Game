import random
import numpy as np
import scipy.stats as stats
from typing import List
# The leeway of their guesses (measured around their expected guess)
leeway  = 2
# Denotes probabilities for the agent distribution:
prob = [0.11,0.35,0.1,0.15,0.03,0.03,0.02,0,0.11,0.1]
class Agent(object):
    def __init__(self):
        self.choice = 0
        super().__init__()
    def choose(self) -> int:
        self.choice = 0
        return 0
    def __str__(self) -> str:
        return "%d from %s" % (self.choice, type(self).__name__)

class NaiveAgent(Agent):
    def __init__(self):
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(100)
        return self.choice

class SmartNaiveAgent(Agent):
    def __init__(self, level = None):
        self.choice = 0
        if level is None: 
            sum = prob[2] + prob[3] + prob[4] + prob[5] + prob[6] + prob[7]
            inner_prob = np.asarray(prob[2:8])
            inner_prob = inner_prob/sum
            level = np.random.choice(6, 1, p = inner_prob)[0]+1
            # level = random.randrange(3)+1
            # level = 1
        self.level = level
        super().__init__()
    
    def choose(self) ->int:
        # print(str(100*((2/3)**self.level))+" "+str(self.level))
        upper_bound = int(100*((2/3)**self.level))
        std = 5**self.level
        
        self.choice = -1
        while self.choice < 0 or self.choice>upper_bound:
            self.choice = round( 
                            (np.random.normal(upper_bound/2, std, 1)[0])
                            )
        
        return self.choice
    def __str__(self) -> str:
        return "%d from %s with level %d" % (self.choice, type(self).__name__, self.level)


class FirstLevelThinker(Agent):
    def __init__(self):
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(leeway)+32
        return self.choice

class SecondLevelThinker(Agent):
    def __init__(self):
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(leeway)+21
        return self.choice

class ThirdLevelThinker(Agent):
    def __init__(self):
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(leeway)+14
        return self.choice

class FourthLevelThinker(Agent):
    def __init__(self):
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(leeway)+9
        return self.choice

class FifthLevelThinker(Agent):
    def __init__(self):
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(leeway)+6
        return self.choice
class SixthLevelThinker(Agent):
    def __init__(self) -> None:
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(leeway)+4
        return self.choice
class SixthLevelThinker(Agent):
    def __init__(self):
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(leeway)+2
        return self.choice

class SeventhLevelThinker(Agent):
    def __init__(self):
        self.choice = 0
        super().__init__()
    
    def choose(self) ->int:
        self.choice = random.randrange(leeway)
        return self.choice

class EmpiricalThinker(Agent):
    def __init__(self, n_friends: int = None, probabilities: List[float] = prob):
        if n_friends is None:
            n_friends = random.randrange(20)+1
        # This is done to avoid reccursively creating empirical agents
        if probabilities[-1] != 0:
            probabilities[0] += (probabilities[-1]/4)
            probabilities[1] += (probabilities[-1]/4)
            probabilities[2] += (probabilities[-1]/4)
            probabilities[3] += (probabilities[-1]/4)
            probabilities[-1] = 0
        self.friends = AgentGenerator.generate_agents_prob(probabilities, n_friends)
        
        self.n_friends = n_friends
        self.probabilities = probabilities
        self.choice = 0
        super().__init__()
    def _helper(self, input: Agent) -> int:
        return input.choose()
    def choose(self) ->int:
        self.choice = int(2*np.average(np.vectorize(self._helper)(self.friends))/3)
        return self.choice
    def __str__(self) -> str:
        out = ""
        for friend in self.friends:
            out+="\t"+ friend.__str__()+"\n"
        return "%d from %s with friends <%d>:\n%s" % (self.choice, type(self).__name__,self.n_friends, out)

class AgentGenerator(object):
    _dictionary = {0: NaiveAgent, 1: SmartNaiveAgent, 2: FirstLevelThinker,
    3: SecondLevelThinker, 4: ThirdLevelThinker, 5: FourthLevelThinker, 6: FifthLevelThinker, 7: SixthLevelThinker, 8: SeventhLevelThinker, 9: EmpiricalThinker}
    def generate_agent(input: int) -> Agent:
        if input > 9 or input<0:
            raise ValueError("Invalid input to generate_agent. Expected value between 0 and 9, but received: %d" % input)
        return AgentGenerator._dictionary[input]()
    
    def generate_agents_prob(input: List[float], n: int) -> List[Agent]:
        if len(input)!=10:
            raise ValueError("Invalid input to generate_agents_prob. Expected list of length 10, but got: %d" % len(input))
        
        
        samples = np.random.choice(10, n, p = input)
        return np.vectorize(AgentGenerator.generate_agent)(samples)

