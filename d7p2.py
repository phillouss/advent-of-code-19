def main():

    outputsArr = []

    settingsArr = genSettings([0,0,0,0,0], 5)
    settingsArr2 = []
    for index in range(0, len(settingsArr) - 4, 5):
        settingsArr2.append([
            settingsArr[index],
            settingsArr[index+1],
            settingsArr[index+2],
            settingsArr[index+3],
            settingsArr[index+4]
        ])

    print(settingsArr2)

    for setting in settingsArr2:
        #print("NEW SETTING")
        outputsArr.append(runFive(setting))

    print(outputsArr)
    biggest = 0

    for number in outputsArr:
        if number > biggest:
            biggest = number

    print("Biggest is {}".format(biggest))


def genSettings(array, step):
    if step == 0 and not repeatingNumbers(array):
        #(array)
        return array

    elif step == 0 and repeatingNumbers:
        return []

    else:
        returnArr = []
        for i in range(5, 10):
            array[step-1] = i
            returnArr.extend(genSettings(array, step - 1))

        return returnArr
        
def repeatingNumbers(array):
    for index in range(len(array)):
        for copy in range(len(array)):
            if copy == index:
                continue
            else:
                if array[copy] == array[index]:
                    return True

    return False

def runFive(inputsArr):
    inputInput = [inputsArr[0], 0]
    amplifiers = []
    i = 0

    for ampName in range(5):
        amplifiers.append(Amplifier())

    while i < 5:
        inputInput = [inputsArr[0 if i > 3 else i + 1], amplifiers[i].runAmplifier(inputInput)]

        if amplifiers[i].exit.done:
            break
        elif i == 4:
            i = 0
        else:
            i += 1
        #print(inputInput)

    return inputInput[1]


class Amplifier:
    def __init__(self):
        inputFile = open("inputtest2.txt", "r", encoding="utf-8")

        input = inputFile.read()
        self.inputArr = []

        for number in input.split(','):
            self.inputArr.append(int(number))

        #print(self.inputArr)
        self.workArray = Computer(self.inputArr)
        self.index = 0
        inputFile.close


    def runAmplifier(self, inputInput):
        '''inputFile = open("inputp1.txt", "r", encoding="utf-8")

        input = inputFile.read()
        inputArr = []

        for number in input.split(','):
            inputArr.append(int(number))

        #print(inputArr)
        workArray = Computer(inputArr)
        
        index = 0'''

        while self.index < len(self.inputArr):
            self.exit = self.workArray.compute(self.index, inputInput)
            #print("computing")
            if self.exit.done:
                #print("DONE: {}, NEXT: {}".format(self.exit.done, self.exit.next))
                break
            if self.exit.changePar:
                self.index = self.exit.par
            else:
                self.index += self.exit.jump
            
            if self.exit.next:
                break



        #print(workArray.input)

        #print(self.workArray.outputOutput)
        return self.workArray.outputOutput

class Computer:
    def __init__(self, arrayName):
        self.input = arrayName
        self.values = ReturnValues(0, False)
        self.outputOutput = 0
        self.inputIndex = 0

    def addStuff(self, operation, index):
        par1 = self.input[index+1] if operation.mod1 == 0 else (index + 1)
        par2 = self.input[index+2] if operation.mod2 == 0 else (index + 2)
        par3 = self.input[index+3] #if operation.mod3 == 0 else (index + 1)

        result = int(self.input[par1]) + int(self.input[par2])
        self.input[par3] = result
        #print("Adding {} + {} to {}".format(par1, par2, par3))

    def multStuff(self, operation, index):
        par1 = self.input[index+1] if operation.mod1 == 0 else (index + 1)
        par2 = self.input[index+2] if operation.mod2 == 0 else (index + 2)
        par3 = self.input[index+3] #if operation.mod3 == 0 else (index + 1)

        result = self.input[par1] * self.input[par2]
        self.input[par3] = result
        #print("Multiplying")
        
    def inputSave(self, operation, index, inputInput):
        par = self.input[index+1] if operation.mod1 == 0 else (index + 1)
        self.input[par] = inputInput[self.inputIndex]
        if self.inputIndex != 0:
            self.values.next = True
        #print("sinput: {} next: {} index: {}".format(self.inputIndex, self.values.next, index))
        self.inputIndex = 1

    def outputPrint(self, operation, index):
        par = self.input[index+1] if operation.mod1 == 0 else (index + 1)
        output = self.input[par]

        self.outputOutput = output
        #else: print("Mode Error")
        #print("Output: {}".format(output))

    def jumpIfTrue(self, operation, index):
        par1 = self.input[index+1] if operation.mod1 == 0 else (index + 1)
        par2 = self.input[index+2] if operation.mod2 == 0 else (index + 2)   
        jumpOrNot = self.input[par1] != 0
        self.values.par = self.input[par2] if jumpOrNot else 0
        return jumpOrNot

    def jumpIfFalse(self, operation, index):
        par1 = self.input[index+1] if operation.mod1 == 0 else (index + 1)
        par2 = self.input[index+2] if operation.mod2 == 0 else (index + 2)
        jumpOrNot = self.input[par1] == 0
        self.values.par = self.input[par2] if jumpOrNot else 0
        return jumpOrNot
    
    def lessThan(self, operation, index):
        par1 = self.input[index+1] if operation.mod1 == 0 else (index + 1)
        par2 = self.input[index+2] if operation.mod2 == 0 else (index + 2)
        par3 = self.input[index+3] #if operation.mod3 == 0 else (index + 1)
        self.input[par3] = 1 if self.input[par1] < self.input[par2] else 0
    def equals(self, operation, index):
        par1 = self.input[index+1] if operation.mod1 == 0 else (index + 1)
        par2 = self.input[index+2] if operation.mod2 == 0 else (index + 2)
        par3 = self.input[index+3] #if operation.mod3 == 0 else (index + 1)
        self.input[par3] = 1 if self.input[par1] == self.input[par2] else 0



    def compute(self, index, inputInput):
        operation = Instructions(self.input[index])
        self.values.next = False
        #print(operation.instructions)

        if operation.instructions == 99:
            print("End")
            self.values.done = True
            self.values.jump = 0
            self.values.changePar = False
            return self.values
        elif operation.instructions == 1:
            self.addStuff(operation, index)
            self.values.done = False
            self.values.jump = 4
            self.values.changePar = False
            return self.values
        elif operation.instructions == 2:
            self.multStuff(operation, index)
            self.values.done = False
            self.values.jump = 4
            self.values.changePar = False
            return self.values

        elif operation.instructions == 3:
            self.inputSave(operation, index, inputInput)
            self.values.done = False
            self.values.jump = 2
            self.values.changePar = False
            
            return self.values

        elif operation.instructions == 4:
            self.outputPrint(operation, index)
            self.values.done = False
            self.values.jump = 2
            self.values.changePar = False
            return self.values

        elif operation.instructions == 5: #jump if true
            self.values.done = False
            self.values.jump = 3
            self.values.changePar = self.jumpIfTrue(operation, index)
            return self.values
        elif operation.instructions == 6: #jump if false
            self.values.done = False
            self.values.jump = 3
            self.values.changePar = self.jumpIfFalse(operation, index)
            return self.values
        elif operation.instructions == 7: #less than
            self.lessThan(operation, index)
            self.values.done = False
            self.values.jump = 4
            self.values.changePar = False
            return self.values
        elif operation.instructions == 8: #equals
            self.equals(operation, index)
            self.values.done = False
            self.values.jump = 4
            self.values.changePar = False
            return self.values
        else:
            print("Error index: {} jump: {}".format(operation.instructions, self.values.jump))
            #print(index)
            self.values.done = True
            #self.values.jump = 0
            return self.values


class ReturnValues():
    def __init__(self, jump, done):
        self.jump = jump
        self.done = done
        self.changePar = False
        self.par = 0
        self.next = False
    
class Instructions:
    def __init__(self, opcode):
        self.instructions = numIndex(opcode, 0) + 10* numIndex(opcode,1)
        self.mod1 = numIndex(opcode, 2)
        self.mod2 = numIndex(opcode, 3)
        self.mod3 = numIndex(opcode, 4)


def numIndex(number, index):
    num = number // 10**index % 10
    return num



if __name__ == "__main__":
    main()
