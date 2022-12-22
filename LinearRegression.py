import numpy as np
import matplotlib.pyplot as plt
n=1000
eps= 1e-8
dim=2
l=-3
r=3
sigma=5
sigmaY=1/sigma**2
sigmaA=sigma/100
sigmaB=sigmaA
max_iterations=1e5

def f(x):
    return 2/np.cosh(np.sinh(np.pi*x[1]))

def h(theta,x):
    return np.dot(theta,x)

def init():
    X=np.ones((n,dim))
    X[:,1::]=np.random.uniform(l,r,size=(n,dim-1))
    X[:,0]=np.ones(n)
    Y=np.zeros(n)
    for i in range(n):
        Y[i]=np.random.normal(f(X[i]),scale=sigmaY,size=1)
    M=np.zeros((n,dim,dim))
    for i in range(n):
        x=X[i:i+1,:]
        M[i]=np.dot(x.transpose(),x)
    return X,Y,M

def A(x):
    a=np.zeros((dim,dim))
    for i in range(n):
        a+=M[i]*np.exp(-np.dot(X[i]-x,X[i]-x) /(2*sigmaA**2))
    return a

def B(x):
    b=np.zeros(dim)
    for i in range(n):
        b+= Y[i]*X[i]*np.exp(-np.dot(X[i]-x,X[i]-x)/(2*sigmaB**2))
    return b

def optimal_solution(theta,x):
    k=0
    a=A(x)
    b=B(x)
    while(k<=max_iterations):
        G = np.dot(a, theta) - b
        m = np.linalg.norm(G)
        if m<=eps:
            break
        step=(m**2)/np.dot(np.dot(a,G),G)
        theta-=step*G
        k+=1

    # print('k =' ,k)
    return theta

def get_solution():
    x = np.ones((n, dim))
    v = np.linspace(l, r, n)
    for i in range(1, dim):
        x[:, i] = v
    p = np.random.uniform(l, r, dim)
    y = np.zeros(n)
    for i in range(n):
        p = optimal_solution(p, x[i])
        y[i] = h(p, x[i])
    return x,y

def show_solution():
    plt.scatter(X[:, 1], Y, marker='.', color='g')
    plt.plot(x[:, 1], y, color='r')
    plt.show()

X,Y,M=init()
x,y=get_solution()
show_solution()