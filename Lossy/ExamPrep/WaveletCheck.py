
import numpy as np
from scipy import misc
from math import sqrt
from math import log2
import matplotlib.pyplot as plt



# put options here, some examples added
N = 4 	# Size of Ks available
Candidates0 = [
	[-0.5, 1.384, 0.007107, 0.5226],
	[0.1, 0.7845, 0.6071, -0.07739],
	[-0.5, 0.1845, 0.6071, -0.6774],
	[0.1, 0.7845, -0.07739, 0.6071]
]

Candidates1 = [
	[-0.2, 0.2514, -0.2929,  0.7443],
	[-0.2, 1.4510, -0.2929,  0.4557],
	[0.4,  0.8514,  0.3071, -0.1443],
	[0.4,  0.8514, -0.1443,  0.3071]
]


Candidates = [
	[ 0.2, 0.8294,  0.5071, -0.1223],
	[ 0.2, 0.8294, -0.1223,  0.5071],
	[-0.2, 0.4294, -0.1071, -0.5223],
	[-0.2, 1.229, -0.1071, -0.2777]
]

Sqrt2 = sqrt(2)

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n################################################")
print("#               Wavelet calculator             #")
print("#               By Miguel Moreno               #")
print("################################################")
print("# The wavelet is the option that complies with #")
print("# ALL THREE conditions!!!                      #")
print("################################################\n\n")
print("---------------------- Condition 1+2 ------------------------")
# Condition 1
for Hk in Candidates:
	print(" --> Cond 1: ", Sqrt2, '==', sum(Hk))
	print(" --> Cond 2: ", 1, '==', sum(map(lambda x: x*x, Hk)), '\n' )




print("----------------------- Condition 3 -------------------------")
# Condition 3
		
for H in Candidates:
	m = 1 # Change this value if needed! For N = 4 don't need to, check PDF for info!
	res = 0
	for k in range(N-2, N):
		res += H[k]*H[k - 2*m]
	print(" --> Cond 3: ", 0, '~=', res )


print(" \n(in case of doubt, pick the one closest to zero) \n\n")
print("-------------------------------------------------------------")
print("#############################################################")
