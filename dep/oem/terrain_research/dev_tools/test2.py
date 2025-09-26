import numpy as np
import matplotlib.pyplot as plt

def double_sigmoid(x, k1=20, c1=0.05, k2=20, c2=0.95):
    sig_left = 1 / (1 + np.exp(-k1 * (x - c1)))
    sig_right = 1 / (1 + np.exp(-k2 * (x - c2)))
    return sig_left * (1 - sig_right)

x = np.linspace(-10, 10, 1000)
y = double_sigmoid(x, k1=30, c1=0.05, k2=30, c2=0.95)

plt.figure(figsize=(8, 4))
plt.plot(x, y, color='red', linewidth=2)
plt.title("Double Sigmoid Function")
plt.xlabel("Input (x)")
plt.ylabel("Output (y)")
plt.grid(True)
plt.show()