#!/usr/bin/python

###############################
# module: random_sampling.py
# description: Starter code for CS3430 HW10
# Robert Epstein
# A01092594
###############################

import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import time

random.seed(int(time.time()))

## age groups
ageGroups = (20, 30, 40, 50, 60, 70)
## number of people in each age group
peopleInAgeGroup = {20:0, 30:0, 40:0, 50:0, 60:0, 70:0}
## number of purchases in each age group
purchasesInAgeGroup = {20:0, 30:0, 40:0, 50:0, 60:0, 70:0}
## total number of purchases
numOfPurchases = 0
## total number of people
numOfPeople = 1000000

def generateAgeDependentSpendingData(nofp):
    global numOfPurchases, ageGroups, numOfPeople
    numOfPeople = nofp
    numOfPurchases = 0
    #resetTables()
    for _ in xrange(numOfPeople):
        ## randomly choose an age group
        ageGroup = random.choice(ageGroups)
        ## the younger you are the less likely you are to buy stuff
        purchaseProbability = float(ageGroup) / 100.0
        ## modify the number of people in ageGroup
        peopleInAgeGroup[ageGroup] += 1
        ## if the purchase probability > random
        if (random.random() < purchaseProbability):
            numOfPurchases += 1
            purchasesInAgeGroup[ageGroup] += 1

def generateAgeIndependentSpendingData(nofp, probOfPurchase=0.4):
    global numOfPurchases, ageGroups, numOfPeople
    numOfPeople = nofp
    numOfPurchases = 0
    #resetTables()
    for _ in xrange(numOfPeople):
        ## randomly choose an age group
        ageGroup = random.choice(ageGroups)
        ## modify the number of people in ageGroup
        peopleInAgeGroup[ageGroup] += 1
        ## if the purchase probability > random
        if (random.random() < probOfPurchase):
            numOfPurchases += 1
            purchasesInAgeGroup[ageGroup] += 1
    pass

## P(Purchase | AgeGroup = x)
def probOfPurchaseGivenAgeGroup(x):
    return float(purchasesInAgeGroup[x])/peopleInAgeGroup[x]

## P(AgeGroup=x)
def probOfAgeGroup(x):
    return float(peopleInAgeGroup[x])/numOfPeople

## P(Purchase) = prob of buying something
def probOfPurchase():
    return float(numOfPurchases)/numOfPeople
 
## P(Purchase, AG=x) 
def probOfPurchaseAndAgeGroup(x):
    return float(purchasesInAgeGroup[x])/numOfPeople

## P(Purchase | AgeGroup = x) = P(Purchase, AgeGroup=x)/P(AgeGroup=x)
def condProbOfPurchaseGivenAgeGroup(x):
    return probOfPurchaseAndAgeGroup(x)/probOfAgeGroup(x)

def arePurchaseAndAgeGroupIndependent(ageGroups, probDiff = 0.01):
    ## your code
    for x in ageGroups:
        diffProbs = abs(condProbOfPurchaseGivenAgeGroup(x) - probOfPurchase())
        if (diffProbs < probDiff):
            print "Purchase and AgeGroup=",x," are independent"
            print "P(Purchase)=",probOfPurchase(),"; P(Purchase|AgeGroup=",x,")=",condProbOfPurchaseGivenAgeGroup(x)
        else:
            print "Purchase and AgeGroup=",x," are dependent"
            print "P(Purchase)=",probOfPurchase(),"; P(Purchase|AgeGroup=",x,")=",condProbOfPurchaseGivenAgeGroup(x)
    pass

def saveDataPlot(nofp, probOfPurchase, dpflag):
    y = []
    for x in ageGroups:
	y.append(probOfPurchaseGivenAgeGroup(x))
    width = 5
    title = 'Purchase Probabilities per Age Group; Sample Size ='+str(nofp)
    plt.title(title)
    plt.ylabel('Probability of Purchase')
    plt.xlabel('Age Group')
    plt.bar(ageGroups, y, width, color="blue")
    fig = plt.gcf()
    plt.plot([10, 80],[probOfPurchase, probOfPurchase], color="red")
    plt.yticks(np.arange( 0, 1.2, .2))

    if dpflag == True:
        filePat = str(nofp)+"_dep.png"
    else:
	filePat = str(nofp)+"_ind.png"
    plt.savefig(filePat)
    pass

    
    
  
def runExperiment(ageGroups, nofp=1000, dependent=True,
                  probOfPurchase=0.4, probDiff=0.1):
    if dependent is True:
        generateAgeDependentSpendingData(nofp)
        arePurchaseAndAgeGroupIndependent(ageGroups, probDiff=probDiff)
        saveDataPlot(nofp, probOfPurchase, dependent)
    else:
        generateAgeIndependentSpendingData(nofp, probOfPurchase=probOfPurchase)
        arePurchaseAndAgeGroupIndependent(ageGroups, probDiff=probDiff)
        saveDataPlot(nofp, probOfPurchase, dependent)

import argparse
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-nofp', '--nofp', required = True, help = 'number of people', type=int)
    ap.add_argument('-pp', '--pp', required = True, help = 'probability of purchase', type=float)
    ap.add_argument('-pd', '--pd', required=True, help='probability difference', type=float)
    ap.add_argument('-dp', '--dp', required=True, help='dependency flag 0/1', type=int) 
    args = vars(ap.parse_args())
    dependency = args['dp']
    if dependency == 0:
        print('Running independent experiment')
        runExperiment(ageGroups, nofp=args['nofp'], dependent=False, probDiff=args['pd'],
                      probOfPurchase=args['pp'])
    elif dependency == 1:
        print('Running dependent experiment')
        runExperiment(ageGroups, nofp=args['nofp'], dependent=True, probDiff=args['pd'])
    else:
        print('Incorrect value for dependency flag %d' % args['dp'])
