def sigmoid(x):
    return 1 / 1 + exp(-x)

def tanh(x):
    print(x)
    answer = (exp(x) - exp(-x)) / (exp(x) + exp(-x))
    print("return: " , answer)
    return answer