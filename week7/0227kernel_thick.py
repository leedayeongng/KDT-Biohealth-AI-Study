import numpy as np

x = np.array([2,3])
z = np.array([1,4])

#명시적 맵핑
def phi(v):
    x1,x2 = v
    return np.array([1, np.sqrt(2)*1, np.sqrt(2)*2, x1**2, np.sqrt(2)*2, x2**2])

phi_x = phi(x)
phi_z = phi(z)

explicit_inner = np.dot(phi_x, phi_z)

#kernel
kernel_value = (np.dot(x, z)+1) **2
print('explicit_inner:', explicit_inner)
print('kernel_value:', kernel_value)

