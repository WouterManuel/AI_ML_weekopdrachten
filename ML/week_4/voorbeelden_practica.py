import numpy as np

'''
naieve implementatie
'''

# theta 0, theta 1
L1 = np.array([0.5, 2])
L2 = np.array([2, 0])
L3 = np.array([0, 0.5])

p1 = np.array([1,1])
p2 = np.array([4,1])
p3 = np.array([3,4])
p4 = np.array([4,4])

# Bereken de voorspelling van punt p1 door hypothese L1
L1[0] + p2[0]*L1[1]

# Bereken de fout van de voorspelling door hypothese L1
(L1[0] + p2[0]*L1[1]) - p2[0]

J_val1 = 0
for p in [p1, p2, p3, p4]:
    h = L1[0] + p[0]*L1[1]  #waarde voorspeld door hypothese L1
    delta = (h - p[1]) ** 2 #kwadrateren van het verschil met de actuele waarde
    J_val1 += delta        #dit verschil optellen bij het totaal
    
J_val1 = J_val1/4  #delen door het aantal observaties
print(J_val1)

'''
vectorieel implementatie
'''
data = np.array([ [1,1], [4,1], [3,4], [4,4] ])
print(data)

# voeg kolom toe met 1-en
data = np.c_[np.ones(4), data]
print(data)

# alle kolommen 0-1
X=data[:, 0:2]
print(X)

y=data[:,[2]]
print(y)

theta = np.array([ [0.5, 2] ])
predictions = np.dot(X, theta.T)
print(predictions)

errors = (predictions - y) ** 2
print(errors)

J_val = sum(errors)/4
print(J_val)

# gegeven een matrix X met waarden van features
# een vector y met actuele uitkomsten voor deze features
# en een vector theta met waarden voor theta
m = y.shape[0] # aantal observaties, als het goed is, is dit hetzelfde als X.shape[0]
predictions = np.dot(X, theta.T)
errors = (predictions - y) ** 2
J_val = sum(errors)/m
print(J_val)
