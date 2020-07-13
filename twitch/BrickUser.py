
from collections import OrderedDict

class BrickUser:
    """ Base class for keeping track of a unique Bricks in the Air user."""

    # Initialization method
    def __init__(self, name, cfg):
        """ Initialization method: note name needs to be unique """

        self.name = str(name)
        self.cfg = cfg
        self.steps = self.cfg["steps"]
        for x in self.steps:
            self.steps[x]["completed"] = False

        #print(self.steps)

        self.currentStepIndex = 1
        self.maxStep = 0
        self.timeOut = 3


    def __eq__(self, other):
        """ Overwrites equal method to check names """
        if (self.name == other.name):
            return True
        else:
            return False

    def matchName(self, name):
        """ Checks to see if the names are identical.  \nReturns True if they match, False otherwise """

        if (self.name == str(name)):
            return True
        else:
            return False

    def getCurrentStep(self):
        """ Returns the current step """
        return self.currentStepIndex

    def getMaxStep(self):
        """ Returns the max step the user has completed """
        return self.maxStep

    def checkAnswer(self, provided_answer):
        """
        Check for a valid answer, if found return true and advance step
        """
        
        for x in self.steps[self.currentStepIndex]["answer"]:
            if x == provided_answer:
                self.currentStepIndex += 1
                return True

        return False

    def getQuestion(self):
        return self.steps[self.currentStepIndex]["question"]

    def getHint(self):
        return self.steps[self.currentStepIndex]["hint"]

    def getAudio(self):
        if "audio" in self.steps[self.currentStepIndex]:
            return self.steps[self.currentStepIndex]["audio"]
        else:
            return None

    def getName(self):
        """ Returns the name """
        return self.name

    def setName(self, name):
        """ Sets the name """
        self.currentStep = str(name)

    def updateTimeout(self):
        """ Subtracts one from the timeout and returns the value """
        self.timeOut = self.timeOut - 1
        return self.timeOut

    def resetTimeout(self):
        """ Resets the timeout to the default value (3) """
        self.timeOut = 3
