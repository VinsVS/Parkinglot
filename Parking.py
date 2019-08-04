class Slot:
    def __init__(self, typ):
        self.type = typ
        self.occupied = False
        self.number = None

    def __repr__(self):
        return self.type + '-' + str(self.occupied) + '-' + str(self.number)


class ParkingGarage:
    def __init__(self):
        self.slots = []
        self.i = 0
        self.j = 0
        self.k = 0
        self.L = 0
        self.R = 0
        self.S = 0

    def takeInput(self):
        print('Enter levels:')
        self.L = int(input(), 10)
        print('Enter Rows:')
        self.R = int(input(), 10)
        print('Enter Slots per Row:')
        self.S = int(input(), 10)
        print(self.L, self.R, self.S)
        print('Enter slots type in row 1: ')
        ip = input()
        lanes = [[Slot(i) for i in ip.split()]]
        x = 1
        while x < self.R:
            print('Enter slots type in row ' + str(x + 1) + ': ')
            ip = input()
            lanes.append([Slot(i) for i in ip.split()])
            x = x + 1

        self.slots = [lanes for i in range(self.L)]

    def printStatus(self):
        for i in range(self.L):
            for j in range(self.R):
                for k in range(self.S):
                    print(self.slots[i][j][k])

    def parkMotorCycle(self, mcNum):
        filled = False
        for i in range(self.L):
            for j in range(self.R):
                for k in range(self.S):
                    if not self.slots[i][j][k].occupied and not filled:
                        self.slots[i][j][k].occupied = True
                        self.slots[i][j][k].number = mcNum
                        filled = True
                        # store on db i, j, k store motorcycle with num mcNum
        return filled

    def parkCar(self, carNum):
        filled = False
        for i in range(self.L):
            for j in range(self.R):
                for k in range(self.S):
                    if not self.slots[i][j][k].occupied and self.slots[i][j][k].type != 'C' and not filled:
                        self.slots[i][j][k].occupied = True
                        self.slots[i][j][k].number = carNum
                        filled = True
                        # store on db i, j, k store  car with num carNum
        return filled

    def parkBus(self, busNum):
        filled = False
        for i in range(self.L):
            for j in range(self.R):
                for k in range(self.S):
                    if not filled and k + 5 <= self.S:
                        fill = True
                        for x in range(k, k + 5):
                            if self.slots[i][j][x].occupied or self.slots[i][j][x].type != 'L':
                                fill = False
                        if fill:
                            for x in range(k, k + 5):
                                self.slots[i][j][x].occupied = True
                                self.slots[i][j][x].number = busNum
                                filled = True

                        # store on db i, j, k - k+5 store  cbus with num busNum
        return filled

    def clearMotorCycleOrCar(self, number):
        cleared = False
        for i in range(self.L):
            for j in range(self.R):
                for k in range(self.S):
                    if self.slots[i][j][k].number == number:
                        self.slots[i][j][k].occupied = False
                        self.slots[i][j][k].number = None
                        cleared = True
                        # clear in db i, j, k with vehicle number number
        return cleared

    def clearBus(self, busNum):
        cleared = False
        for i in range(self.L):
            for j in range(self.R):
                for k in range(self.S):
                    if not cleared and k + 5 <= self.S:
                        contain = True
                        for x in range(k, k + 5):
                            if self.slots[i][j][x].number != busNum:
                                contain = False
                        if contain:
                            for x in range(k, k + 5):
                                self.slots[i][j][x].occupied = False
                                self.slots[i][j][x].number = None
                                cleared = True

                        # store on db i, j, k - k+5 store  cbus with num busNum
        return cleared


def runPG(typ, number):
    if (typ == 'C'):
        if pg.parkCar(number):
            print('successfully parked')
        else:
            print('No slot available')

    if (typ == 'M'):
        if pg.parkMotorCycle(number):
            print('successfully parked')
        else:
            print('No slot available')

    if (typ == 'B'):
        if pg.parkBus(number):
            print('successfully parked')
        else:
            print('No slot available')

    if (typ == 'CC'):
        if pg.clearMotorCycleOrCar(number):
            print('successfully cleared')
        else:
            print('Not Found')

    if (typ == 'CM'):
        if pg.clearMotorCycleOrCar(number):
            print('successfully cleared')
        else:
            print('Not Found')

    if (typ == 'CB'):
        if pg.clearBus(number):
            print('successfully cleared')
        else:
            print('Not Found')


print('Usage:')
print('1. Enter levels, Row, Slots per row')
print('2. Enter Slots type in each row e.g. M C L (motorcycle slot, compact slot and large slot)')
print('3. Start using convention -> <code vehicle-number>, e.g. C 21 park car with number 21')
print('4. Available codes:')
print('C - park car\nM - park motorcycle\nB - park bus')
print('CC - clear Car\nCM - clear motorcycle\nCB - clear bus')
pg = ParkingGarage()
pg.takeInput()
pg.printStatus()

while True:
    print('Enter Code:')
    inp = input().split()
    print('Code ', inp[0], 'vehicle number', inp[1])
    runPG(inp[0], inp[1])
    pg.printStatus()