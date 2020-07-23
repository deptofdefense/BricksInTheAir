# Code for managing twitch user list
# Created for defcon28 Aerospace Village

import time # needed for sleep
import threading # needed for userThread
import random # needed for zone generation
from BrickUser import BrickUser

class UserList:
    """ List of active users """

    def __init__(self, cfg, dispMan):
        """ init method """

        self.cfg = cfg
        self.dispMan = dispMan
        self.userList = []
        #self.currentUser = BrickUser("temp", self.cfg)
        self.currentUser = None
        self.limit = cfg["cue"]["limit"]
        self.time_allowed = cfg["cue"]["time"]
        self.current_user_lock = threading.Lock()
        self.cue_lock = threading.Lock()

    def addUser(self, name):
        """ Checks if user already exists, and if not adds them to the list.  \nReturns True if name is added, False otherwise """

        self.cue_lock.acquire()
        for user in self.userList:
            if (user.matchName(name)):
                self.cue_lock.release()
                return False

        #if user list is empty
        if not self.userList:
            self.setCurrentUser(BrickUser(name, self.cfg))

        if len(self.userList) < self.limit:
            print("adding new user:" + name)
            self.userList.append(BrickUser(name, self.cfg))
            self.dispMan.updateUserList(self.getNextUserList(5))
            print(self.userList)
            self.cue_lock.release()
            return True
        else:
            self.cue_lock.release()
            return False

    def removeUser(self, name):
        ''' Checks if user already exists and removes them from the list.  \nReturns true if removed, false otherwise '''
        self.cue_lock.acquire()
        print("remove name: " + name)
        print(self.userList)
        for user in self.userList:
            if (user.matchName(name)):
                self.userList.remove(user)
                self.dispMan.updateUserList(self.getNextUserList(5))
                print("found the user, returning true")
                self.cue_lock.release()
                return True

        print("returning false")
        self.cue_lock.release()
        return False

    def startUserThread(self):
        """ Starts the user thread """
        print("Start userList thread")

        t = threading.Thread(target=self.userThread, daemon=True)
        t.start()

    def userThread(self):
        """ Runs through list and updates the current user every 60 seconds """

        while True:
            if len(self.userList) > 0:
                self.cue_lock.acquire()
                user = self.userList.pop()
                self.cue_lock.release()

                self.setCurrentUser(user)

                if (user.updateTimeout() >= 0):
                    self.cue_lock.acquire()
                    self.userList.append(user)   #put them at the end
                    self.cue_lock.release()
                    time.sleep(self.time_allowed)
                else:
                    pass    #already removed with the pop() above
                #self.lock.release()
                self.dispMan.updateUserList(self.getNextUserList(5))

    def getCurrentUser(self):
        """ Grabs the current user as dictated by userThread """
        with self.current_user_lock:
            return self.currentUser

    def setCurrentUser(self, user):
        """ Grabs the current user as dictated by userThread """
        with self.current_user_lock:
            self.currentUser = user

    def getUserList(self):
        """ Returns the list of current Users """
        with self.cue_lock:
            return self.userList

    def getNextUserList(self, nextCount):
        ''' Returns the next X users in the list formated by Name : time \nnextCount : how long the next user list should be '''
        msg = ""
        for x in self.userList:
            msg += x.getName() + "\n"
        print("active user list: " + msg)
        return msg
