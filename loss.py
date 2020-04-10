import numpy as np

def rmspe(y_true, y_pred):
    '''
    Calculating the Root Mean Squared Percentage Error
    
    Input: y_true, y_pred --> numpy array
    Output: loss --> double value
    '''
    loss = np.sqrt(np.mean(np.square(((y_true - y_pred) / max(y_true,1))), axis=0))

    return loss

def ape(y_true, y_pred):
    '''
    Calculating the Absolute Percentage Error
    
    Input: y_true, y_pred --> list
    Output: loss --> numpy float64
    '''

    loss = 0
    
    for i in range(len(y_true)):
        loss += abs(y_true[i] - y_pred[i]) / max(y_true[i], 1)
    loss = loss / len(y_true)

    return loss