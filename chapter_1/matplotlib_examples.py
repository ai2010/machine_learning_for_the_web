import matplotlib.pyplot as plt
import numpy as np
#first example: 1 line plot
plt.plot([10,5,2,4],color='green',label='line 1', linewidth=5)
plt.ylabel('y',fontsize=40)
plt.xlabel('x',fontsize=40)
plt.axis([0,3, 0,15])
plt.show()
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
ax.set_xlabel('x',fontsize=40)
ax.set_ylabel('y',fontsize=40)
fig.suptitle('figure',fontsize=40)
ax.plot([10,5,2,4],color='green',label='line 1', linewidth=5)
fig.savefig('figure.png')


#second example: multiple lines plot
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
r = np.arange(0., 10., 0.3)
p1, = ax.plot(r, r, 'r--',label='line 1', linewidth=10)
p2, = ax.plot(r, r**0.5, 'bs',label='line 2', linewidth=10)
p3, = ax.plot(r,np.sin(r),'g^', label='line 3', markersize=10)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels,fontsize=40)
ax.set_xlabel('x',fontsize=40)
ax.set_ylabel('y',fontsize=40)
fig.suptitle('figure 1',fontsize=40)
fig.savefig('figure_multiplelines.png')


#third example: scatter plot with random points
colors = ['b', 'c', 'y', 'm', 'r']
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(np.random.random(10), np.random.random(10), marker='x', color=colors[0])
p1 = ax.scatter(np.random.random(10), np.random.random(10), marker='x', color=colors[0],s=50)
p2 = ax.scatter(np.random.random(10), np.random.random(10), marker='o', color=colors[1],s=50)
p3 = ax.scatter(np.random.random(10), np.random.random(10), marker='o', color=colors[2],s=50)
ax.legend((p1,p2,p3),('points 1','points 2','points 3'),fontsize=20)
ax.set_xlabel('x',fontsize=40)
ax.set_ylabel('y',fontsize=40)
fig.savefig('figure_scatterplot.png')
