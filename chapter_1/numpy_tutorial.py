import numpy as np
import time

#test speed
def sum_trad():
    start = time.time()
    X = range(10000000)
    Y = range(10000000)
    Z = []
    for i in range(len(X)):
        Z.append(X[i] + Y[i])
    return time.time() - start
    
def sum_numpy():
    start = time.time()
    X = np.arange(10000000) 
    Y = np.arange(10000000) 
    Z=X+Y
    return time.time() - start

print 'time sum:',sum_trad(),'  time sum numpy:',sum_numpy()

#array creation
arr = np.array([2, 6, 5, 9], float)
print arr
print type(arr)
arr = np.array([1, 2, 3], float)
print arr.tolist()
print list(arr)
arr = np.array([1, 2, 3], float)
arr1 = arr
arr2 = arr.copy()
arr[0] = 0
print arr
print arr1
print arr2
arr = np.array([10, 20, 33], float)
print arr
arr.fill(1)
print arr
print np.random.permutation(3)
print np.random.normal(0,1,5)
print np.random.random(5)

print np.identity(5, dtype=float)
print np.eye(3, k=1, dtype=float)

print np.ones((2,3), dtype=float)
print np.zeros(6, dtype=int)
arr = np.array([[13, 32, 31], [64, 25, 76]], float)
print np.zeros_like(arr)
print np.ones_like(arr)
arr1 = np.array([1,3,2])
arr2 = np.array([3,4,6])
print np.vstack([arr1,arr2])
print np.random.rand(2,3)
print np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[5,])

#array manipulations
arr = np.array([2., 6., 5., 5.])
print arr[:3]
print arr[3]
arr[0] = 5.
print arr
print np.unique(arr)
print np.sort(arr)
print np.argsort(arr)
np.random.shuffle(arr)
print arr
print np.array_equal(arr,np.array([1,3,2]))
matrix = np.array([[ 4., 5., 6.], [2, 3, 6]], float)
print matrix
print matrix[0,0],'--',matrix[0,2]
arr = np.array([[ 4., 5., 6.], [ 2., 3., 6.]], float)
print arr[1:2,2:3]
print arr[1,:]
print arr[:,2]
print arr[-1:,-2:]
arr = np.array([[10, 29, 23], [24, 25, 46]], float)
print arr
print arr.flatten()
print arr.shape
print arr.dtype
int_arr = matrix.astype(np.int32)
print int_arr
arr = np.array([[ 4., 5., 6.], [ 2., 3., 6.]], float)
print len(arr)
arr = np.array([[ 4., 5., 6.], [ 2., 3., 6.]], float)
print 2 in arr
print 0 in arr
arr = np.array(range(8), float)
print arr
arr = arr.reshape((4,2))
print arr
print arr.shape
arr = np.array(range(6), float).reshape((2, 3))
print arr
print arr.transpose()
matrix = np.arange(15).reshape((3, 5))
print matrix
print matrix .T
arr = np.array([14, 32, 13], float)
print arr
print arr[:,np.newaxis]
print arr[:,np.newaxis].shape
print arr[np.newaxis,:]
print arr[np.newaxis,:].shape

arr1 = np.array([10,22], float)
arr2 = np.array([31,43,54,61], float)
arr3 = np.array([71,82,29], float)
print np.concatenate((arr1, arr2, arr3))

arr1 = np.array([[11, 12], [32, 42]], float)
arr2 = np.array([[54, 26], [27,28]], float)
print np.concatenate((arr1,arr2))
print np.concatenate((arr1,arr2), axis=0)
print np.concatenate((arr1,arr2), axis=1)

arr = np.array([10, 20, 30], float)
str = arr.tostring()
print str
print np.fromstring(str)

#arrays operations
arr1 = np.array([1,2,3], float)
arr2 = np.array([1,2,3], float)
print arr1+arr2
print arr1–arr2
print arr1 * arr2
print arr2 / arr1
print arr1 % arr2
print arr2**arr1
arr1 = np.array([1,2,3], float)
arr2 = np.array([1,2], float)
print arr1 + arr2
arr1 = np.array([[1, 2], [3, 4], [5, 6]], float)
arr2 = np.array([1, 2], float)
print arr1
print arr2
print arr1 + arr2
arr1 = np.zeros((2,2), float)
arr2 = np.array([1., 2.], float)
print arr1
print arr2
print arr1+arr2
print arr1 + arr2[np.newaxis,:]
print arr1 + arr2[:,np.newaxis]
arr = np.array([[1, 2], [5, 9]], float)
print arr >= 7
print arr[arr >= 7]
arr[np.logical_and(arr > 5, arr < 11)]
print arr

arr1 = np.array([1, 4, 5, 9], float)
arr2 = np.array([0, 1, 1, 3, 1, 1, 1], int)
print arr1[arr2]
arr = np.array([1, 4, 5, 9], float)
print arr[[0, 1, 1, 3, 1]]

arr1 = np.array([[1, 2], [5, 13]], float)
arr2 = np.array([1, 0, 0, 1], int)
arr3 = np.array([1, 1, 0, 1], int)
print arr1[arr2,arr3]
arr1 = np.array([7, 6, 6, 9], float)
arr2 = np.array([1, 0, 1, 3, 3, 1], int)
print arr1.take(arr2)
arr1 = np.array([[10, 21], [62, 33]], float)
arr2 = np.array([0, 0, 1], int)
print arr1.take(arr2, axis=0)
print arr1.take(arr2, axis=1)
arr1 = np.array([2, 1, 6, 2, 1, 9], float)
arr2 = np.array([3, 10, 2], float)
arr1.put([1, 4], arr2)
print arr1
arr1 = np.array([[11,22], [23,14]], float)
arr2 = np.array([[25,30], [13,33]], float)
print arr1*arr2

#linear algebra operations
X = np.arange(15).reshape((3, 5))
print X
print X.T
print np.dot(X .T, X)#X^T X

arr1 = np.array([12, 43, 10], float)
arr2 = np.array([21, 42, 14], float)
print np.outer(arr1, arr2)
print np.inner(arr1, arr2)
print np.cross(arr1, arr2)

matrix = np.array([[74, 22, 10], [92, 31, 17], [21, 22, 12]], float)
print matrix
print np.linalg.det(matrix)
inv_matrix = np.linalg.inv(matrix)
print inv_matrix
print np.dot(inv_matrix,matrix)
vals, vecs = np.linalg.eig(matrix)
print vals
print vecs

#Statistics and mathematical functions
arr = np.random.randn(8, 4)
print arr.mean()
print np.mean(arr)
print arr.sum()

