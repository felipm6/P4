import matplotlib.pyplot as plt

# coeficientes LP
X, Y = [], []
for line in open('lpout.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(1)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('LP',fontsize=18)
plt.xlabel('coef 1')
plt.ylabel('coef 2')
plt.savefig('lpout.png')
plt.show()

# coeficientes LPCC
X, Y = [], []
for line in open('lpccout.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(2)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('LPCC',fontsize=18)
plt.xlabel('coef 1')
plt.ylabel('coef 2')
plt.savefig('lpccout.png')
plt.show()

# coeficientes MFCC
X, Y = [], []
for line in open('mfccout.txt', 'r'):
  values = [float(s) for s in line.split()]
  X.append(values[0])
  Y.append(values[1])
plt.figure(3)
plt.plot(X, Y, 'b*', markersize=4)
plt.title('MFCC',fontsize=18)
plt.xlabel('coef 1')
plt.ylabel('coef 2')
plt.savefig('mfccout.png')
plt.show()