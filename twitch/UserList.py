# Code for managing twitch user list
# Created for defcon28 Aerospace Village

import time # needed for sleep
import threading # needed for userThread
import random # needed for zone generation
import asyncio # needed for async ops

from BrickUser import BrickUser

class UserList:
    """ List of active users """

    def __init__(self, cfg, dispMan, bot):
        """ init method """

        self.cfg = cfg
        self.dispMan = dispMan
        self.bot = bot
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
            print("adding new user:" + name)
            newUser = BrickUser(name, self.cfg)
            self.userList.append(newUser)
            self.cue_lock.release()
            self.setCurrentUser(newUser)
            self.triggerChanges()

        if len(self.userList) < self.limit:
            print("adding new user:" + name)
            self.userList.append(BrickUser(name, self.cfg))
            self.triggerChanges()
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

                print("found the user, returning true")
                self.cue_lock.release()

                self.current_user_lock.acquire()
                if user == self.currentUser:
                    # need to remove/adjust who currentUser actually is
                    if len(self.userList) > 0:
                        self.currentUser = self.userList[0]
                    else:
                        self.currentUser = None
                self.triggerChanges()

                self.current_user_lock.release()
                return True
        self.triggerChanges()
        self.cue_lock.release()
        return False

    def triggerChanges(self):
        self.dispMan.updateUserList(self.getNextUserList(5))
        if self.currentUser != None:
            self.dispMan.updateImage(self.currentUser.getImage())
        else:
            self.dispMan.updateImage(None)

    def startUserThread(self):
        """ Starts the user thread """
        print("Start userList thread")

        t = threading.Thread(target=self.userThread, args=(), daemon=True)
        t.start()

    def userThread(self):
        """ Runs through list and updates the current user every X seconds """
        while True:
            print("********************************servicing userthread")

            if len(self.userList) > 0:
                self.cue_lock.acquire()
                user = self.userList.pop(0) # remove the first user in the list
                self.cue_lock.release()

                self.setCurrentUser(user)
                time.sleep(self.time_allowed)

                if (user.updateTimeout() >= 0):
                    self.cue_lock.acquire()
                    self.userList.append(user)   #put them at the end
                    self.cue_lock.release()


                else:
                    print("removing user for inactivity: " + str(user))
                    try:
                        msg = "Removing " + user.getName() + " for inactivity."
                        asyncio.run(self.bot._ws.send_privmsg(self.bot.initial_channels[0], msg))
                    except Exception as err:
                        pass

                self.dispMan.updateUserList(self.getNextUserList(5))
                if self.currentUser != None:
                    self.dispMan.updateImage(self.currentUser.getImage())

            else:
                #print("no active users")
                time.sleep(1)
                try:
                    self.dispMan.updateImage(None)
                    self.currentUser = None
                except Exception as err:
                    print("error inializing dispMan")
                    print(repr(err))



    def getCurrentUser(self):
        """ Grabs the current user as dictated by userThread """
        with self.current_user_lock:
            return self.currentUser

    def setCurrentUser(self, user):
        """ Grabs the current user as dictated by userThread """
        print("setting current user: " + str(user))
        with self.current_user_lock:
            self.currentUser = user
            self.triggerChanges()

    def getUserList(self):
        """ Returns the list of current Users """
        with self.cue_lock:
            return self.userList

    def getNextUserList(self, nextCount):
        ''' Returns the next X users in the list formated by Name : time \nnextCount : how long the next user list should be '''

        msg = ""
        self.cue_lock.acquire()
        for x in self.userList:
            msg += x.getName() + "\n"
        self.cue_lock.release()
        print("active user list: " + msg)
        return msg
