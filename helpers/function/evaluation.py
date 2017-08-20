from numpy import sqrt, square, sum

def RMSE(prediction, compare):
    err = sum(square(compare - prediction))
    rmse = sqrt(err / prediction.shape[0])
    return rmse