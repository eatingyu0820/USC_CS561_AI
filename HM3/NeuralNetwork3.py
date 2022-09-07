import sys
import numpy as np
np.random.seed(42)
from numpy import genfromtxt,array, savetxt

#Training and test data accepted from cmd arguments
X_train = genfromtxt(str(sys.argv[1]), delimiter=',')
Y_train = genfromtxt(str(sys.argv[2]), delimiter=',')
X_test = genfromtxt(str(sys.argv[3]), delimiter=',')

#Normalize training data into 0-1 range
X_train=X_train/255.0

#One hot encoding of the Y_trian
a=np.zeros((Y_train.shape[0],10))
for i in range(Y_train.shape[0]):
    j=int(Y_train[i])
    a[i][j]=1
Y_train=a


#Softmax
def softmax(z):
    epow=np.exp(z-z.max())
    return epow/np.sum(epow,axis=0)

#Derivative of softmax
def softmax_derivative(z):
    epow=np.exp(z-z.max())
    return epow/np.sum(epow,axis=0)*(1-epow/np.sum(epow,axis=0))

#Sigmoid
def sigmoid(z):
    return 1/(1+np.exp(-z))    

#Sigmoid Derivatice
def sigmoid_derivative(z):
    return (np.exp(-z))/((1+np.exp(-z))**2)

epochs = 5
l_rate = 1
np.random.seed(0)
scale = 1/max(1., (2+2)/2.)
limit = np.sqrt(3.0 * scale)
W1=np.random.uniform(-limit, limit, size=(128,784))
W2=np.random.uniform(-limit, limit, size=(64,128))
W3=np.random.uniform(-limit, limit, size=(10,64))


for iteration in range(epochs):
    for x,y in zip(X_train, Y_train):
        #Forward Propagation
        A0 = x
        Z1= np.dot(W1, A0)
        A1 = sigmoid(Z1)
        Z2= np.dot(W2, A1)
        A2 = sigmoid(Z2)
        Z3= np.dot(W3, A2)
        A3 = softmax(Z3)
        #Backward propagation
        error = 2 * (A3 - y) / A3.shape[0] * softmax_derivative(Z3)
        W3-= l_rate *np.outer(error, A2)
        error = np.dot(W3.T, error) * sigmoid_derivative(Z2)
        W2-= l_rate *np.outer(error, A1)
        error = np.dot(W2.T, error) * sigmoid_derivative(Z1)
        W1-= l_rate *np.outer(error, A0)



predictions = []
for x in X_test:
        #Forward pass
        A0 = x
        Z1= np.dot(W1, A0)
        A1 = sigmoid(Z1)
        Z2= np.dot(W2, A1)
        A2 = sigmoid(Z2)
        Z3= np.dot(W3, A2)
        A3 = softmax(Z3)
        pred = np.argmax(A3)
        predictions.append(pred)
#Save predictions        
savetxt('test_predictions.csv', predictions, delimiter='\n', fmt='%i')



