import o

#### Parameters ####

Uu, Uf = 20, 80 # Uu: n following >= num following of X percent of users

T = 20 # tweets stored for each account. don't store retweets

n = 4000 # minimum distinct challenges in a row (max items in bloom)

R, rrr = 3, 0.01 # acceptabel num of iterations, rrr percent of the time


print "twters", Uu + Uf

tweets = (Uu + Uf) * T
print "tweets", tweets

space = o.I(T, Uu, Uf)
print "space:", space

Preal = o.P_r(n, space)
print "Preal:", Preal

P_one = o.P_one(R, rrr)
print "P_one:", P_one

Pfals = o.P_f(P_one, Preal)
print "Pfals:", Pfals

moptk = o.m(n, Pfals)
print "moptk:", moptk

k = o.k(moptk, n)
print "k    : {} ({})".format(round(k), k)

mrealk = o.m_k(n, round(k), Pfals)
print "mrealk", mrealk

caught = Preal * n
print 'caught', int(round(caught))

fiter = Pfals * n
print 'extras', int(round(fiter))
