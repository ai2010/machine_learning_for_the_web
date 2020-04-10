import numpy as np
from copy import copy

class HMM:
    def __init__(self,pi,A,B):
        self.pi = pi
        self.A = A
        self.B = B
        
    def MostLikelyStateSequence(self,observations):
        
        #calc combinations:
        N = self.A.shape[0]
        T = len(observations)
        sequences = [str(i) for i in range(N)]
        probs = np.array([self.pi[i]*self.B[i,observations[0]] for i in range(N)])
        print probs
        for i in range(1,T):
            newsequences = []
            newprobs = np.array([])
            for s in range(len(sequences)):
                for j in range(N):
                    newsequences.append(sequences[s]+str(j))
                    bef = int(sequences[s][-1])
                    tTpprob = probs[s]*self.A[bef,j]*self.B[j,observations[i]]
                    newprobs = np.append(newprobs,[tTpprob]) 
                    print sequences[s]+str(j),'-',tTpprob
            sequences = newsequences
            probs = newprobs
        return max((probs[i],sequences[i]) for i in range(len(sequences)))
            
    def ViterbiSequence(self,observations):
        deltas = [{}]
        seq = {}
        N = self.A.shape[0]
        states = [i for i in range(N)]
        T = len(observations)
        #initialization
        for s in states:
            deltas[0][s] = self.pi[s]*self.B[s,observations[0]]
            seq[s] = [s]
        #compute Viterbi
        for t in range(1,T):
            deltas.append({})
            newseq = {}
            for s in states:
                (delta,state) = max((deltas[t-1][s0]*self.A[s0,s]*self.B[s,observations[t]],s0) for s0 in states)
                deltas[t][s] = delta
                newseq[s] = seq[state] + [s]
            seq = newseq
            
        (delta,state) = max((deltas[T-1][s],s) for s in states)
        return  delta,' sequence: ', seq[state]
        
    def maxProbSequence(self,observations):
        N = self.A.shape[0]
        states = [i for i in range(N)]
        T = len(observations)
        M = self.B.shape[1]
        # alpha_t(i) = P(O_1 O_2 ... O_t, q_t = S_i | hmm)
        # Initialize alpha
        alpha = np.zeros((N,T))
        c = np.zeros(T) #scale factors
        alpha[:,0] = pi.T * self.B[:,observations[0]]
        c[0] = 1.0/np.sum(alpha[:,0])
        alpha[:,0] = c[0] * alpha[:,0]
        # Update alpha for each observation step
        for t in range(1,T):
            alpha[:,t] = np.dot(alpha[:,t-1].T, self.A).T * self.B[:,observations[t]]
            c[t] = 1.0/np.sum(alpha[:,t])
            alpha[:,t] = c[t] * alpha[:,t]

        # beta_t(i) = P(O_t+1 O_t+2 ... O_T | q_t = S_i , hmm)
        # Initialize beta
        beta = np.zeros((N,T))
        beta[:,T-1] = 1
        beta[:,T-1] = c[T-1] * beta[:,T-1]
        # Update beta backwards froT end of sequence
        for t in range(len(observations)-1,0,-1):
            beta[:,t-1] = np.dot(self.A, (self.B[:,observations[t]] * beta[:,t]))
            beta[:,t-1] = c[t-1] * beta[:,t-1]
            
        norm = np.sum(alpha[:,T-1])
        seq = ''
        for t in range(T):
            g,state = max(((beta[i,t]*alpha[i,t])/norm,i) for i in states)
            seq +=str(state)
            
        return seq
        
    def simulate(self,time):

        def drawFromNormal(probs):
            return np.where(np.random.multinomial(1,probs) == 1)[0][0]

        observations = np.zeros(time)
        states = np.zeros(time)
        states[0] = drawFromNormal(self.pi)
        observations[0] = drawFromNormal(self.B[states[0],:])
        for t in range(1,time):
            states[t] = drawFromNormal(self.A[states[t-1],:])
            observations[t] = drawFromNormal(self.B[states[t],:])
        return observations,states


    def train(self,observations,criterion):

        N = self.A.shape[0]
        T = len(observations)
        M = self.B.shape[1]

        A = self.A
        B = self.B
        pi = copy(self.pi)
        
        convergence = False
        while not convergence:

            # alpha_t(i) = P(O_1 O_2 ... O_t, q_t = S_i | hmm)
            # Initialize alpha
            alpha = np.zeros((N,T))
            c = np.zeros(T) #scale factors
            alpha[:,0] = pi.T * self.B[:,observations[0]]
            c[0] = 1.0/np.sum(alpha[:,0])
            alpha[:,0] = c[0] * alpha[:,0]
            # Update alpha for each observation step
            for t in range(1,T):
                alpha[:,t] = np.dot(alpha[:,t-1].T, self.A).T * self.B[:,observations[t]]
                c[t] = 1.0/np.sum(alpha[:,t])
                alpha[:,t] = c[t] * alpha[:,t]

            #P(O=O_0,O_1,...,O_T-1 | hmm)
            P_O = np.sum(alpha[:,T-1])
            # beta_t(i) = P(O_t+1 O_t+2 ... O_T | q_t = S_i , hmm)
            # Initialize beta
            beta = np.zeros((N,T))
            beta[:,T-1] = 1
            beta[:,T-1] = c[T-1] * beta[:,T-1]
            # Update beta backwards froT end of sequence
            for t in range(len(observations)-1,0,-1):
                beta[:,t-1] = np.dot(self.A, (self.B[:,observations[t]] * beta[:,t]))
                beta[:,t-1] = c[t-1] * beta[:,t-1]

            gi = np.zeros((N,N,T-1));

            for t in range(T-1):
                for i in range(N):
                    
                    gamma_num = alpha[i,t] * self.A[i,:] * self.B[:,observations[t+1]].T * \
                            beta[:,t+1].T
                    gi[i,:,t] = gamma_num / P_O
  
            # gamma_t(i) = P(q_t = S_i | O, hmm)
            gamma = np.squeeze(np.sum(gi,axis=1))
            # Need final gamma element for new B
            prod =  (alpha[:,T-1] * beta[:,T-1]).reshape((-1,1))
            gamma_T = prod/P_O
            gamma = np.hstack((gamma,  gamma_T)) #append one Tore to gamma!!!

            newpi = gamma[:,0]
            newA = np.sum(gi,2) / np.sum(gamma[:,:-1],axis=1).reshape((-1,1))
            newB = copy(B)
            
            sumgamma = np.sum(gamma,axis=1)
            for ob_k in range(M):
                list_k = observations == ob_k
                newB[:,ob_k] = np.sum(gamma[:,list_k],axis=1) / sumgamma

            if np.max(abs(pi - newpi)) < criterion and \
                   np.max(abs(A - newA)) < criterion and \
                   np.max(abs(B - newB)) < criterion:
                convergence = True;
  
            A[:],B[:],pi[:] = newA,newB,newpi

        self.A[:] = newA
        self.B[:] = newB
        self.pi[:] = newpi
        self.gamma = gamma
        

if __name__ == '__main__':
       
    pi = np.array([0.6, 0.4])
    A = np.array([[0.7, 0.3],
                           [0.6, 0.4]])
    B = np.array([[0.7, 0.1, 0.2],
                           [0.1, 0.6, 0.3]])
    hmmguess = HMM(pi,A,B)
    print 'Viterbi sequence:',hmmguess.ViterbiSequence(np.array([0,1,0,2]))
    print 'max prob sequence:',hmmguess.maxProbSequence(np.array([0,1,0,2]))    
    #obs,states = hmmguess.simulate(4)
    
    hmmguess.train(np.array([0,1,0,2]),0.000001)

    print 'Estimated initial probabilities:',hmmguess.pi

    print 'Estimated state transition probabililities:',hmmguess.A

    print 'Estimated observation probabililities:',hmmguess.B