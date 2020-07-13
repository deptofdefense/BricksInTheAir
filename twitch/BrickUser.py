
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

    def setCurrentStep(self, desired_step):
        if desired_step <= len(self.steps) and desired_step >= 1:
            self.currentStepIndex = desired_step
            return "Step: {} set.".format(desired_step)
        else:
            return "Invalid step requested."

    def getMaxStep(self):
        """ Returns the max step the user has completed """
        return self.maxStep

    def checkAnswer(self, provided_answer):
        """
        Check for a valid answer, if found return true and advance step
        """

        # this is a bizzare question... any answer outside of an otehrwise valid range is the answer
        if "answer_lower" in self.steps[self.currentStepIndex] and "answer_upper" in self.steps[self.currentStepIndex]:
            parts = provided_answer.split()
            answer = self.steps[self.currentStepIndex]["answer"].split()

            answer_total_len = len(answer) + 1
            if len(parts) != answer_total_len:
                return False

            for i in range(len(answer)):
                if parts[i] != answer[i]:
                    return False

            compare = parts[-1]
            print(compare)
            if compare < self.steps[self.currentStepIndex]["answer_lower"] or compare > self.steps[self.currentStepIndex]["answer_upper"]:
                return True

        else:
            for x in self.steps[self.currentStepIndex]["answer"]:
                if x == provided_answer:
                    return True

        return False

    def getFakeI2CResponse(self):
        if "fake_i2c_response" in self.steps[self.currentStepIndex]:
            return self.steps[self.currentStepIndex]["fake_i2c_response"]
        else:
            return None

    def incrementCurrentStepIndex(self):
        self.currentStepIndex += 1
        if self.maxStep < self.currentStepIndex:
            self.maxStep = self.currentStepIndex


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
