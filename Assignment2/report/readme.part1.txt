b)
For every dependence, (i,j), having i<j, one is the head, and one is the child, search every node pairs (y,z) where i<y<j, and z<i or z>j, if the dependence (y,z) exist in the graph, then it is non-projective and return false. After searching every pairs and did not return false, then the graph is projective, and return true.

c)
example that is projective:
I drink teas rather than coffee.
Parsing result:
nsubj(drink-2, I-1)
root(ROOT-0, drink-2)
dobj(drink-2, teas-3)
cc(teas-3, rather-4)
mwe(rather-4, than-5)
conj(teas-3, coffee-6)

example that is non-projective:
What I said is used by him.
Parsing result:
dobj(said-3, What-1)
nsubjpass(used-5, What-1)
nsubj(said-3, I-2)
root(ROOT-0, said-3)
auxpass(used-5, is-4)
ccomp(said-3, used-5)
agent(used-5, him-7)