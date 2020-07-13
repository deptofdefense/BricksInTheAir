# Code for managing twitch user list
# Created for defcon28 Aerospace Village

import time # needed for sleep
import threading # needed for userThread
import random # needed for zone generation
from BrickUser import BrickUser

class UserList:
    """ List of active users """

    def __init__(self, cfg):
        """ init method """

        self.cfg = cfg
        self.userList = []
        self.currentUser = BrickUser("temp", self.cfg)

    def addUser(self, name):
        """ Checks if user already exists, and if not adds them to the list.  \nReturns True if name is added, False otherwise """

        for user in self.userList:
            if (user.matchName(name)):
                return False

        #if user list is empty
        if not self.userList:
            self.setCurrentUser(BrickUser(name, self.cfg))

        self.userList.append(BrickUser(name, self.cfg))
        return True

    def removeUser(self, name):
        ''' Checks if user already exists and removes them from the list.  \nReturns true if removed, false otherwise '''

        for user in self.userList:
            if (user.matchName(name)):
                self.userList.remove(user)
                return True

        return False

    def startUserThread(self):
        """ Starts the user thread """

        t = threading.Thread(target=self.userThread, daemon=True)
        t.start()

    def userThread(self):
        """ Runs through list and updates the current user every 60 seconds """

        tempUser = BrickUser("temp", self.cfg)

        while True:
            for user in self.userList:
                if (user.updateTimeout() >= 0):
                    self.currentUser = user
                    time.sleep(60)
                else:
                    self.userList.remove(user)

            # done to make sure current user is never null
            self.currentUser = tempUser

    def getCurrentUser(self):
        """ Grabs the current user as dictated by userThread """

        return self.currentUser

    def setCurrentUser(self, user):
        """ Grabs the current user as dictated by userThread """

        self.currentUser = user

    def getUserList(self):
        """ Returns the list of current Users """

        return self.userList

    def getNextUserList(self, nextCount):
        ''' Returns the next X users in the list formated by Name : time \nnextCount : how long the next user list should be '''

        startPoint = 0

        if nextCount > len(self.userList):
            nextCount = len(self.userList)

        for user in self.userList:
            if user.matchName(self.currentUser.name):
                break
            else:
                startPoint = startPoint + 1

        if (startPoint >= len(self.userList)) or (len(self.userList) == 0):
            return "N/A"

        msg = ""
        for i in range(nextCount):
            msg = msg + f"\n{self.userList[startPoint].getName()} : {i} min "
            startPoint = startPoint + 1

            if startPoint >= len(self.userList):
                startPoint = 0

        return msg
