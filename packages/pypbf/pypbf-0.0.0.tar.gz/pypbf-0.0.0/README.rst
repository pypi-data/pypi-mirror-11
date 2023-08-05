pypbf is a python package implementing the probabilistic bloom filter, which is a type of probabilistic data structure. The PBF supports frequency estimation on items, hence could identify which items are frequent, of which frequency exceeds the user-specified threshold.

The paper which proposed the PBF is following.

Yanjun Yao, Sisi Xiong, Jilong Liao, Micheal Berry, Hairong Qi, Qing Cao, Identifying Frequent Flows in Large Datasets through Probabilistic Bloom Filters. IEEE International Symposium on Quality of Service 2015.

The PBF is an extension of classic bloom filter. The key difference is that whenever an item is inserted, instead of flipping the hash locations from 0 to 1 deterministically, we introduce a new parameter p, ranging from 0 to 1, which controls the probability to flip the bits. In implementation, we generate a random number ranging from 0 to 1, and compared it to a preset parameter p. If the random number is less than p, we flip bit. Otherwise, the bit remain the same.

In the query frequency operation, we count how many bits have been set to 1 out of k hashed postions, and then calculate frequency.

Usage:
>>> from pypbf import PBF
>>> pbf = PBF(n = 1000, f = 100, k = 200) #Construct a pbf with total number of items = 1000, threshold frequency = 100, default number of hash functions = 200, user could also specify. 
>>> pbf.insert('foo') # insert 'foo' to pbf, return True if the number of items inserted has not exceeded the capacity of the pbf
True
>>> count = pbf.numItems() #return the number of items have been inserted to the pbf
1
>>> freq = pbf.queryFreq('foo') #return the frequency of 'foo'
1


