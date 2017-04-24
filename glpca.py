import scipy.sparse.linalg as splinalg
import scipy.sparse as sparse

class GLPCA():
  """
  Implements the algorithm by Jiang et al. 2013
  """
  def __init__(self, n_components, beta):
    self.n_components = n_components
    self.beta = beta

  def fit_transform(self, X, L):
    if L.shape[0] != L.shape[1] or L.shape[0] != X.shape[1]:
      raise ValueError("Laplacian matrix is of wrong shape")
    XtX = X.T.dot(X)
    n = XtX.shape[0]
    lambda_n= splinalg.eigh(XtX, k=1, which='LM')[0][0]
    eta_n = splinalg.eigh(L, k=1, which='LM')[0][0] #Largest eigenvalues of XtX and L, respectively
    
    newmat = (1 - self.beta)*(sparse.eye(n) - XtX/lambda_n) + (self.beta)*(L/eta_n)
    newd, newv = splinalg.eigh(newmat, k=self.n_components, which='SM')
    self.U = X.dot(newv)
    self.Qt = newv.T
    return self.U

  def inverse_transform(self, U):
    return U.dot(self.Qt)
