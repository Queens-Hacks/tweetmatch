from math import log, exp

# size of inputs
I = lambda T, Uu, Uf: T * ((Uu + Uf) ** 2 - (Uu + Uf))

# max probability of positive for one iteration
P_one = lambda R, Pt: Pt ** (1.0 / R)

# probability of positive
P_r = lambda n, s: (n - 1.0) / s

# max probability of false positive
P_f = lambda P_o, P_r: P_o - P_r

# size of bloom filter wit optimal k
m = lambda n, P: n * log(1.0 / P) / log(2) ** 2

# number of hashes
k = lambda m, n: m / float(n) * log(2)

# size of bloom filter with real k
#def m_k(n, k, P):

m_k = lambda n, k, P: -(k * n) / log(1 - P ** (1 / float(k)))
