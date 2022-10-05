"""Various memory utilities using a dictionary format."""

import functools
import operator
import json

import Utilities

#backup for MDF erase
backup = {}

#master dictionary file location
mdfl = "C:\\Users\\jacob\\OneDrive\\Desktop\\Project\\MUN\\MDF.txt"

class MDF:
    """
    General memory processing class, with open and close being necessary for access.

    Open arguments cause the command to open the file once and close it once the actions are complete.
    It is preferable, if more than one command needs the memory to be open, to wrap Memory.memory.open() and Memory.memory.close() around instead.
    """
    #master dictionary file

    def __init__(self, location):
        """
        Starts the MDF class by establishing the location of the memory file.

        location: str (file location)
        """
        self.location = location

    def store(self, keys, information, open=False):
        """
        Writes the information to the MDF using the key(s) that were provided in a list, with the last key being the key that the information is written to.

        keys: list
        open: bool

        *Memory should be open.
        """
        if open:
            self.open()
        #Makes sure everything is a string
        #for index,item in enumerate(keys):
            #keys[index] = str(item)
        #Adds the information to the master dictionary
        self.cmdf = Utilities.atnd(self.cmdf, keys, information)
        #Converts the dictionary back to a string
        #string cmdf
        #Original behavior: scmdf = str(self.cmdf)
        #Remove the old information
        self.mdf.truncate()
        #Write the new information
        #Original behavior: self.mdf.write(scmdf)
        json.dump(self.cmdf, self.mdf)
        #Return back to the beginning of the file after reading it
        self.mdf.seek(0)
        if open:
            self.close()

    def retrieve(self, keys, open=False):
        """
        Reads the specified key in the MDF, returning the information.

        keys: list
        open: bool

        *Memory should be open, even though it being closed would not cause an error, because opening memory updates the cmdf with any recent changes.
        """
        if open:
            self.open()
        #Makes sure everything is a string
        #for index,item in enumerate(keys):
            #keys[index] = str(item)
        #Attempts to get the information at the key
        #try:
        information = functools.reduce(operator.getitem, keys, self.cmdf)
        #except:
            #print(f"Error in retrieve method of class MDF, no such keys '{keys}' exist.")
            #return "Error in MDF retrieve"
        if open:
            self.close()
        return information

    def remove(self, keys, open=False):
        """
        Removes the specific key in the MDF, returning the information at the key in case it is needed.

        keys: list
        open: bool

        *Memory should be open.
        """
        if open:
            self.open()
        #Makes sure everything is a string
        #Lists make this a problem, try without it
        #for index,item in enumerate(keys):
            #keys[index] = str(item)
        #Attempts to get the information at the key and remove it
        #try:
        #try:
        #Get the information
        information = self.retrieve(keys)
        #Remove the information
        self.cmdf = Utilities.rfnd(self.cmdf, keys)
        #except:
            #if open:
                #self.close()
            #return
        #Converts the dictionary back to a string
        #string cmdf
        #Original behavior: scmdf = str(self.cmdf)
        #Remove the old information
        self.mdf.truncate()
        #Write the new information
        #Original behavior: self.mdf.write(scmdf)
        json.dump(self.cmdf, self.mdf)
        #Return back to the beginning of the file after reading it
        self.mdf.seek(0)
        #except:
            #print(f"Error in the remove method of class MDF, no such keys '{keys}' exist.")
            #return "Error in MDF remove"
        if open:
            self.close()
        return information

    def erase(self, open=False):
        """
        Erases the MDF and replaces it with an empty dictionary, keeping a backup in the global backup variable that can be accessed temporarily.

        open: bool

        *Memory should be open.
        *Warning: this removes all memory information!
        ***Likely a temporary function.
        ***Backup variable is likely temporary, too.
        """
        if open:
            self.open()
        global backup
        #Truncate the entirety of the file
        self.mdf.truncate()
        #Write the new empty dictionary
        self.mdf.write("'{}'")
        #Return back to the beginning of the filer after writing to it
        self.mdf.seek(0)
        #Backup cmdf in case it was on accident
        backup = self.cmdf
        #Update cmdf
        self.cmdf = {}
        if open:
            self.close()

    def close(self):
        """Closes the MDF."""
        self.mdf.close()

    def open(self):
        """Access the MDF by opening it and getting the dictionary, necessary prior to any other memory usage."""
        self.mdf = open(self.location, "r+")
        #content mdf
        #Original behavior: self.cmdf = self.mdf.read()
        try:
            self.cmdf = json.load(self.mdf)
        except json.decoder.JSONDecodeError:
            self.cmdf = {}
        #Return to the beginning of the file after reading it
        self.mdf.seek(0)
        #Original behavior:
        #if self.cmdf == '':
        #    self.cmdf = "{}"
        #Converts the string to a dictionary
        #self.cmdf = eval(self.cmdf)
        if not type(self.cmdf) == type({}):
            #Original behavior: self.erase()
            self.cmdf = {}

class User:
    """
    User memory access class, with shortcuts for accessing user specific memory information.

    Open arguments cause the command to open the file once and close it once the actions are complete.
    It is preferable, if more than one command needs the memory to be open, to wrap Memory.memory.open() and Memory.memory.close() around instead.
    """

    def __init__(self, open=False):
        """
        Starts the User class by getting the current user from memory or by input, while also adding a blank dictionary for the user if it did not exist previously.

        open: bool

        *Memory should be opened.
        """
        global memory
        if open:
            memory.open()
        try:
            self.name = memory.retrieve(['currentuser'])
        except:
            #Causes error, circular import related, also not needed here: Screen.inputscreen("User Name")
            while True:
                name = input("User: ")
                if not name == '':
                    break
            self.setcurrentuser(name)
        try:
            memory.retrieve(['users',self.name])
        except:
            memory.store(['users',self.name], {})
        if open:
            memory.close()

    def lfm(self, noi, open=False):
        """
        Gets the information at the specified area provided in the noi variable, see 'MDF.retrieve' in this module for the underlying function.

        noi: list
        open: bool

        *Memory should be opened.
        """
        #load from memory
        global memory
        if open:
            memory.open()
        #name of information
        accessl = ['users', self.name]
        accessl += noi
        information = memory.retrieve(accessl)
        if open:
            memory.close()
        return information

    def atm(self, noi, information, open=False):
        """
        Sets the information at the specified area provided in the noi variable, see 'MDF.store' in this module for the underlying function.

        noi: list
        open: bool

        *Memory should be opened.
        """
        #add to memory
        global memory
        if open:
            memory.open()
        #name of information
        accessl = ['users', self.name]
        accessl += noi
        memory.store(accessl, information)
        if open:
            memory.close()

    def rfm(self, noi, open=False):
        """
        Removes the information at the specified area provided in the noi variable and returns it for optional use, see 'MDF.remove' in this module for the underlying function.

        noi: list
        open: bool

        *Memory should be opened.
        """
        #remove from memory
        global memory
        if open:
            memory.open()
        #name of information
        accessl = ['users', self.name]
        accessl += noi
        information = memory.remove(accessl)
        if open:
            memory.close()
        return information

    def setcurrentuser(self, name, open=False):
        """
        Sets the current user stored in memory, used when the application is first loaded to determine which user to use.

        open: bool

        *Memory should be opened.
        """
        global memory
        if open:
            memory.open()

        self.name = name
        memory.store(['currentuser'], name)
        if open:
            memory.close()

#Set up memory
memory = MDF(mdfl)

#Set up active user
#main user
mu = User(True)
