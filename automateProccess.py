#!/usr/bin/python

import subprocess, sys
import time

'''
!!!!!!! I HIGHLY RECOMMEND NEVER DOING THIS !!!!! -- find alternatives where possible
nano {yourscriptname}.sh
        #!/bin/bash

            if [ "$1" == 'run' ];then
                do something
            fi

            if [ "$1" == 'stop' ];then
                do something
            fi
chmod +x {yourscriptname}.sh
!!!!!!!SCARY BIT - HIGHLY RECOMMEND AGAINST!!!!!!! -- ENSURE PERMISSIONS ARE SETUP CORRECTLY
sudo nano /etc/sudoers
    yourusername ALL=(root) NOPASSWD: /location/to/script.sh
'''

class ServiceCmds:

    #Making the functionality and commands be initialized as an object (Useless in it's current state, but functionality for more servers is going to be added)
    def __init__(self,cmd):

        self.cmd = cmd
        self.error = 'Invalid: {errCmd}\nError: {errPoint}\nUsage: [ operation ] [ target ]\nExample: python3 automateProccess.py run both -- runs app and the server.'
        self.validCmds = {
            #I have duplicated this as in the future, more servers will be added and different cmds for run/stop will need to be added.
            'run': ['mc','srv','both'],
            'stop': ['mc','srv','both']
            }
        #Gets the localIP to open the web interface
        self.localip = ((str((subprocess.check_output(['hostname', '--all-ip-addresses']))).split(' '))[0]).replace("b'", "")
        
        #bash commands to start server, services, etc... (again, setup like this for the ease of adding to it in the future)
        self.runCmds = {
            'service':'sudo /home/dir/dir/dir {shCmd}',
            'mc': "java -jar /home/dir/dir/jar",
            'browserOpn': 'firefox ' +'https://'+ self.localip+':8443/panel/dashboard' #Web interface to server and app.
        }


    #Parsing my arguments as I seem to typo a lot. This will show you where in the command you went wrong and provide usage examples and Error codes.
    def ArgsParse(self):

        try:
            try:
                self.cmd.remove('automateProccess.py')
            except:
                self.error = 'Please run from the command line'
                return self.error
            if (self.cmd[0] in ['run', 'stop']):
                #Checking is less than 3 but more than 1 arguments are supplied (range of args script can deal wtih)
                if len(self.cmd) >= 3 or (checkLenArgs := len(self.cmd) == 1):
                    if checkLenArgs == True:
                        #Check if a target is specified then if not return false and update error attribute
                        self.error = self.error.format(errCmd=self.cmd[0], errPoint='<-- no targets specified')
                        return False
                    #Return and update error attribute if too many are applied
                    self.error = self.error.format(errCmd=self.cmd, errPoint=(self.cmd + ' <-- too many arguments'))
                    return False
                #Checking through the validCmds attribute for each key:value and ensuring there's no invalid args
                for i in range(1, len(self.cmd)):
                    if (self.cmd[i] in self.validCmds['run'] or self.cmd[i] in self.validCmds['stop']):
                        #Pass if valid
                        pass
                    else:
                        #Return False update error attribute
                        self.error = self.error.format(errCmd=self.cmd[i], errPoint=(self.cmd[i] + '<-- is not a valid target')) 
                        return False   
                #Below is if all is successful, update the cmd attribute for the object with a dictionary
                self.cmd = {'operation': self.cmd[0], 'target': self.cmd[1]} 

            #If run or stop isn't provided first or at all, return False update error attribute
            else:
                self.error = self.error.format(errCmd=self.cmd[0], errPoint=(self.cmd[0] +'<-- is not an operation')) 
                return False     
        except:
            #Exception block for if no args at all are applied (operation, target) Return False update error attribute.
            self.error = self.error.format(errCmd='see below', errPoint='No arguments supplied!')
            return self.error
        

    #Rather pointless but in 1% chance the service doesn't start, I added a timer so you don't get an unreachable error.
    def browser(self):
        #Give it 5 seconds, usual in my testing. Max was about 3, but just in-case.
        n = 5
        for i in range(0,5):
            print('Opening browser in: '+ str(n-i) + ' second(s)....')
            time.sleep(1)
        #See attributes in the __init__ function, browserOpn cmd just opens firefox at localhost IP    
        subprocess.Popen(self.runCmds['browserOpn'] , shell=True,stdout=subprocess.PIPE)


    #The 'main' class function, take it the operation from the arguments and run commands based on dict: self.runCmds attr.
    def run(self):
        if(self.cmd['operation'] == 'run'):
            if (self.cmd['target'] == 'mc'):
                #Open app alone
                subprocess.Popen(self.runCmds['mc'] , shell=True,stdout=subprocess.PIPE)
            if (self.cmd['target'] == 'srv'):
                #openSrv and web interface
                subprocess.Popen(self.runCmds['service'].format(shCmd=self.cmd['operation']) , shell=True,stdout=subprocess.PIPE)
                self.browser()
            if (self.cmd['target'] == 'both'):
                #Open app, srv and web interface
                subprocess.Popen(self.runCmds['mc'], shell=True,stdout=subprocess.PIPE)
                subprocess.Popen(self.runCmds['service'].format(shCmd=self.cmd['operation']), shell=True,stdout=subprocess.PIPE)
                self.browser()
        if(self.cmd['operation'] == 'stop'):
            #If stopped, only attempt to close the system service - web interface and app will follow.
            subprocess.Popen(self.runCmds['service'].format(shCmd=self.cmd['operation']), shell=True,stdout=subprocess.PIPE)
            print('Service shutdown, close java manually.')
        



def main(argsObj):
    #If classmethod ArgsParse returns something other than None(signalling an error), print it out
    if argsObj.ArgsParse() != None:
        print(argsObj.error)
        quit()

    #Run the main class function
    argsObj.run()

if __name__ == '__main__':
    #Assigning the args to a class object
    cmdStatus = ServiceCmds(sys.argv)
    #running the script as a whole.
    main(cmdStatus)

