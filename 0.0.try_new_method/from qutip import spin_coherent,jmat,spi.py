from qutip import spin_coherent,jmat,spin_q_function,plot_spin_distribution_3d,mesolve
import numpy as np
import matplotlib.pyplot as plt

n=2#原子数
j = n//2
psi0 = spin_coherent(j, np.pi/2, 0)#设置初态,自旋相干态
Jz=jmat(j,"z")
H=Jz**2#系统的哈密顿量

tlist=np.linspace(0,1,100)#时间列表
result=mesolve(H,psi0,tlist)#态随时间的演化

theta=np.linspace(0, np.pi, 100)
phi=np.linspace(0, 2*np.pi, 100)
Q1, THETA1, PHI1 = spin_q_function(result.states[0], theta, phi)
Q2, THETA2, PHI2 = spin_q_function(result.states[30], theta, phi)
Q3, THETA3, PHI3 = spin_q_function(result.states[60], theta, phi)
Q4, THETA4, PHI4 = spin_q_function(result.states[90], theta, phi)

fig = plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(221,projection='3d')
ax2 = fig.add_subplot(222,projection='3d')
ax3 = fig.add_subplot(223,projection='3d')
ax4 = fig.add_subplot(224,projection='3d')

plot_spin_distribution_3d(Q1, THETA1, PHI1,fig=fig,ax=ax1)
plot_spin_distribution_3d(Q2, THETA2, PHI2,fig=fig,ax=ax2)
plot_spin_distribution_3d(Q3, THETA3, PHI3,fig=fig,ax=ax3)
plot_spin_distribution_3d(Q4, THETA4, PHI4,fig=fig,ax=ax4)

for ax in [ax1,ax2,ax3,ax4]:
    ax.view_init(0.5*np.pi, 0)
    ax.axis('off')#不显示坐标轴
#fig.savefig("1.png",dpi=400)
plt.show()
