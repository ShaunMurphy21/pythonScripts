import pyautogui
from glob import glob
import time
import keyboard
import sys
import random

class testCases:

    def __init__(self, operation):

        self.operation = operation
        self.invalidCases = glob(r'../img/*_invalid_*.png')
        self.validCases = glob(r'../img/*_valid_*.png')
        self.testValidCases = glob(r'../img/valids/*_valid_*.png')
        self.testInvalidCases = glob(r'../img/valids/*_invalid_*.png')
        self.manipulation = None
        self.cases = []

    def genData(self):
        pathName = r'../img/testCases/{id}_{valid}_pic{counter}.png'
        pathName0 = r'../img/valids/{id}_{valid}_pic{counter}.png'
        pathName1 = r'../img/invalids/{id}_{valid}_pic{counter}.png'
        i = 0
        valid = 0
        invalid = 0

        while True:
            n = random.randint(0,100000)
            print(f'Valid: {valid}\nInvalid: {invalid}')
            if keyboard.is_pressed('ctrl'):
                im = pyautogui.screenshot(region=(890,490, 150, 150))
                im.save(pathName.format(id=n,valid='valid',counter=valid))
                im.save(pathName0.format(id=n,valid='valid',counter=valid))
                valid = valid + 1
                time.sleep(0.050)
            else:
                im = pyautogui.screenshot(region=(890,490, 150, 150))
                im.save(pathName.format(id=n,valid='invalid',counter=invalid))
                im.save(pathName1.format(id=n,valid='invalid',counter=invalid))
                invalid = invalid + 1
                i = i + 1
                time.sleep(0.200)

    def validPredicts(self):
        pathName = r'../img/valids/{id}_valid_pic{counter}.png'
        i = 0

        while True:
            n = random.randint(0,100000)
            if keyboard.is_pressed('ctrl'):
                im = pyautogui.screenshot(region=(890,490, 150, 150))
                im.save(pathName.format(id=n, counter=i))
                i = i + 1
                print(f'Valid test cases: '+pathName.format(id=n, counter=i))
                time.sleep(0.050)
            else:
                print('sleeping...')
                time.sleep(0.100)

    def run(self):

        if self.operation[1] == 'valid_predictions':
            self.validPredicts()
        if self.operation[1] == 'training_data':
            self.genData()
        if self.operation[1] == 'manipulate_data':
            #self.manipImg()
            pass




#sys.argv ----- arguments ran from CMDLine ---- e.g, sudo python3 caseGen.py validpredicts       -- generate valid predictions


def main(argsObjs):
    cmdStats.run()



if __name__ == '__main__':

    cmdStats = testCases(sys.argv)
    
    main(cmdStats)