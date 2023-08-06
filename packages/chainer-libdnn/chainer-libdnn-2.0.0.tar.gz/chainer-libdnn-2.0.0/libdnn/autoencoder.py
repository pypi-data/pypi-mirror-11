# coding: utf-8
# Simple chainer interfaces for Deep learning researching
# For autoencoder
# Author: Aiga SUZUKI <ai-suzuki@aist.go.jp>

import chainer
import chainer.functions as F
import chainer.optimizers as Opt
import numpy
from libdnn.nnbase import NNBase


class AutoEncoder(NNBase):
    def __init__(self, model, gpu=-1):
        NNBase.__init__(self, model, gpu)

        self.optimizer = Opt.Adam()
        self.optimizer.setup(self.model)

        self.loss_function = F.mean_squared_error
        self.loss_param = {}

    def validate(self, x_data, train=False):
        y = self.forward(x_data, train=train)
        if self.gpu >= 0:
            x_data = chainer.to_gpu(x_data)

        x = chainer.Variable(x_data)

        return self.loss_function(x, y, **self.loss_param)

    def train(self, x_data, batchsize=100, action=(lambda: None)):
        N = len(x_data)
        perm = numpy.random.permutation(N)

        sum_error = 0.

        for i in range(0, N, batchsize):
            x_batch = x_data[perm[i:i + batchsize]]

            self.optimizer.zero_grads()
            err = self.validate(x_batch, train=True)

            err.backward()
            self.optimizer.update()

            sum_error += float(chainer.cuda.to_cpu(err.data)) * batchsize
            action()

        return sum_error / N

    def test(self, x_data, action=(lambda: None)):
        err = self.validate(x_data, train=False)
        action()

        return float(chainer.cuda.to_cpu(err.data))
