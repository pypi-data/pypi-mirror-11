#
# @author jonathan_lee@berkeley.edu (Jonathan N. Lee)
# 
# NetworkBase module that defines an abstract network. sizes parameter determines
# the number of nodes in each respective layer. layers by default
# consist of an inputs and mlps with sigmoid activations.
#
# Please do not implement "NotImplemented" code blocks; they are not implemented
# for a reason...
# 


# system libraries
import random
import json
# internal libraries
import layers
import activations
import colors
import costs
# third party libraries
import numpy as np
import matplotlib.pyplot as plt

def output(s=""):
    print colors.green + str(s) + colors.end

# list2vec converts a list of any dimension to a numpy array
# that is also a column vector (mx1 matrix where m equals the
# number of elements in li. also will put non-lists into a list
# 
# try converting obj to np array and reshaping. if type error,
# then convert obj to list then np array and reshape and return.
def list2vec(li):
    try:
        li = np.array(li)
        return np.reshape(li, (len(li), 1))
    except TypeError:
        li = np.array([li])
        return np.reshape(li, (len(li), 1))

# convert an data type (such as a tuple or even
# an int!) to a list.
def it2list(iterable):
    try:
        it = iter(iterable[0])
        return list(iterable[0])
    except TypeError:
        return list(iterable)

# reconstruct json from a given file
# in the form of the saved Network structure
# see "save" function
# returns a constructed network model
def load(path):
    with open(path) as in_file:
        layers = json.load(in_file)
    net = Network( [ layers[0]['size'] ] )
    for layer in layers[1:]:
        size = layer['size']
        activ = layer['activ']
        type_ = layer['type']
        net.append(size, type_, activ)
        if layer['b'] is not None:  net.end.b = np.array(layer['b'])
        else:                       net.end.b = None
        if layer['w'] is not None:  net.end.w = np.array(layer['w'])
        else:                       net.end.w = None
    return net
        


class NetworkBase(object):

    # initialize the network by creating
    # a layers with the corresponding number of nodes
    # @params sizes     list of positive integers representing
    #                   nodes per layer
    def __init__(self, sizes):
        raise NotImplementedError


    # propagate forward by iterating over all layers
    # staring with the first layer
    # @param x          input column vector
    def forward(self, x):
        raise NotImplementedError

    # create and append layer to the end layer of the network
    # simply by using the end instance variable
    # see layers.py and activations.py for mappings
    # @param size       number of nodes in the layer
    # @param type_      layer identifier type    
    # @param activ      activation identifier type
    # type_ and activ are optional
    def append(self, *args):
        raise NotImplementedError

    # pop the last layer off the network
    # by setting end instance var to the 
    # previous layer and removing the previous
    # layers forward propagation to this
    def pop(self):
        raise NotImplementedError

    # train neural network based on training data
    # to optimize the weights. Abstract method
    # intended to be handled by implementing network
    # class
    # @param training_set       training_set which is a list
    #                           of tuples: first component is column
    #                           input vec, second is column output vec
    # @param epochs             number of iterations to update weights
    # @param alpha              learning rate
    # @param mini_batch_size    by default, reverts to 1
    # @param monitor            by default, no loss surveillence
    def train(self, *args):
        raise NotImplementedError

    # iterate through layer and update the biases
    # and weights as each layer type should handle
    # the individual implementation uniquely
    # applying the delta updates should always zero
    # out the delta weights
    # @param alpha              learning rate
    def _apply_updates(self, alpha):
        raise NotImplementedError

    # iterate through each alyer and zero out
    # the weights, as handled by the implementations
    # of the given layers
    def _zero_deltas(self):
        raise NotImplementedError

    # iterate through each layer and save the weights
    # and biases to a specified text file in the file_path
    # will also store the network hyperparameters
    # @param file_path      path to the write file
    def save(self, file_path):
        raise NotImplementedError

    # load weights and biases from a specified file path
    # Note: this overwrites the current network structure
    # and weights and biases. Use carefully.
    # @param file_path      path to the read file
    def load(self, file_path):
        raise NotImplementedError

    # compute the cost given a 
    def _compute_cost(self, training_set):
        raise NotImplementedError

    # convert the network to json format, essentially
    # just by saving information in string/number format
    def toJSON(self):
        raise NotImplementedError

    # save the network by structuring the network
    # as a list of dictionaries. dictionaries would
    # then easily be converted to json and later
    # reconstructed into a Network object
    def save(self, path):
        raise NotImplementedError



# Network class provides the implementation of NetworkBase's 
# non implemented functions. See interface class for details about
# each funciton (no comments in this class provided)
class Network(NetworkBase):


    def __init__(self, *args):
        sizes = it2list(args)
        it = iter(sizes)
        self.start = layers.Input(next(it))              
        layer = self.start
        for size in it:
            layer.append( layers.MLP(size, activations.sigmoid) )
            layer = layer.next_
        self.end = layer


    def forward(self, *args):
        x = it2list(args)
        x = list2vec(x)
        it = iter(self.start)
        for layer in it:
            x = layer.forward(x)
        return it2list(x)


    def append(self, *args):
        size = args[0]
        if len(args) > 1:   type_ = args[1]
        else:               type_ = "mlp"       # default argument
        if len(args) > 2:   activ = args[2]
        else:               activ = "sigmoid"   # default argument
        
        type_ = layers.mapping[type_]
        activ = activations.mapping[activ]
        layer = type_(size, activ)
        self.end.append(layer)
        self.end = self.end.next_


    def pop(self):
        self.end = self.end.prev
        self.end.append(None)


    def train(self, training_set, epochs, alpha, mini_batch_size=1, monitor=False):
        training_set = [ ( list2vec(x), list2vec(y) ) for x, y in training_set]
        self.costcurve = []
        alpha = float(alpha)
        n = len(training_set)
        self._zero_deltas()
        for j in xrange(epochs):
            random.shuffle(training_set)
            mini_batches = [
                training_set[k:k + mini_batch_size] 
                for k in xrange(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self._update_batch(mini_batch, alpha)
            if monitor:
                output("Epoch " + str(j) + " compeleted")
                self.costcurve.append(self._compute_cost(training_set))

    def show_cost(self):
        x = xrange(0, len(self.costcurve), 1)
        plt.plot(x, self.costcurve)
        plt.show()


    def _update_batch(self, training_set, alpha):
        for x, y in training_set:
            self.forward(x)
            mu = costs.mean_square.deriv(self.end.x, y) *\
                self.end.activ.deriv(self.end.z)
            root = self.end
            while root is not None:
                mu = root._backward(mu)
                root = root.prev
        self._apply_updates(alpha/len(training_set))


    def _apply_updates(self, alpha):
        it = iter(self.start)
        for layer in it:
            layer._apply_updates(alpha)
            layer._zero_deltas()


    def _zero_deltas(self):
        it = iter(self.start)
        for layer in it:
            layer._zero_deltas()


    def _compute_cost(self, training_set):
        cost = 0
        for x, y in training_set:
            actual = self.forward(x)
            cost += np.linalg.norm(costs.mean_square.func(actual, y))
        return cost / len(training_set)

    def __len__(self):
        return len(self.start)
        
    
    def toJSON(self):
        it = iter(self.start)
        layers = []
        for layer in it:
            layers.append(layer.toJSON())
        return layers

        
    def save(self, path):
        netJSON = self.toJSON()
        with open(path, 'w') as outfile:
            json.dump(netJSON, outfile)
    

    """# --TODO--
    def save(path):
        it = iter(self.start)
        layers = []
        for layer in it:
            layers.append(layer)
        with open(path, 'w') as outfile:
            json.dump(layers, outfile)
"""
