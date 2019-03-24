import os
import sys

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")
sys.path.append(base_dir)

from src.classifiers.KernelLR import KernelLogisticRegression
from src.classifiers.KernelSVM import KernelSVM

choices = {'kernel-lr': KernelLogisticRegression,
           'kernel-svm': KernelSVM}


def choose(name):
    return choices[name]
