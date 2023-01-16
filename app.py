from flask import Flask
from bs4 import BeautifulSoup
import requests
from ast import literal_eval
from prettytable import PrettyTable
import itertools

r = requests.get('https://usis.bracu.ac.bd/academia/admissionRequirement/getAvailableSeatStatus')
soup = BeautifulSoup(r.content,"html.parser")

text_table = soup.find("table")

text_table = text_table.text.split('\n')
text_table = [text_table[i] for i in range(0, len(text_table)) if text_table[i] != '']
table = [text_table[i:i+10] for i in range(0, len(text_table), 10)]

# with open('table.txt', 'w') as t:
#     t.writelines(str(table))

# with open('table.txt', 'r') as f:
#     lines = f.readlines()

# lines = literal_eval(lines[0])
# for x in range(len(lines)-1):
#     lines[x].pop(-1)

# print(table[:20])
class Course:
    def __init__(self, arr):
        self.CourseCode = arr[0]
        self.Program = arr[1]
        self.Faculty = arr[2]
        self.Credit = arr[3]
        self.Section = arr[4]
        self.DayTimeRoom = arr[5]
        self.TotalSeat = arr[6]
        self.SeatBooked = arr[7]
        self.SeatRemaining = arr[8]
        self.ClassTimes = []
        self.LabDate = ''
        self.ClassRoom = []
        self.CheckLab()
        self.setClssDateTime()


    def CheckLab(self):
        x = self.DayTimeRoom.split(') ')
        if sum('Sa' in s for s in x) > 1:
            self.labExists = True
            self.LabDate += 'Saturday'
        elif sum('Su' in s for s in x) > 1:
            self.labExists = True
            self.LabDate += 'Sunday'
        elif sum('Mo' in s for s in x) > 1:
            self.labExists = True
            self.LabDate += 'Monday'
        elif sum('Tu' in s for s in x) > 1:
            self.labExists = True
            self.LabDate += 'Tuesday'
        elif sum('We' in s for s in x) > 1:
            self.labExists = True
            self.LabDate += 'Wednesday'
        elif sum('Th' in s for s in x) > 1:
            self.labExists = True
            self.LabDate += 'Thursday'
        else:
            self.labExists = False
            self.LabDate += 'None'
    
    def setClssDateTime(self):
        x = self.DayTimeRoom.split(') ')
        for y in x:
            var = ''
            if 'Sa' in y:
                var += '0.'
            elif 'Su' in y:
                var+='1.'
            elif 'Mo' in y:
                var += '2.'
            elif 'Tu' in y:
                var += '3.'
            elif 'We' in y:
                var += '4.'
            elif 'Th' in y:
                var += '5.'

            if '08:00 AM-09:20 AM' in y:
                var += '0'
            elif '09:30 AM-10:50 AM' in y:
                var += '1'
            elif '11:00 AM-12:20 PM' in y:
                var += '2'
            elif '12:30 PM-01:50 PM' in y:
                var += '3'
            elif '02:00 PM-03:20 PM' in y:
                var += '4'
            elif '03:30 PM-04:50 PM' in y:
                var += '5'
            elif '05:00 PM-06:20 PM' in y:
                var += '6'
            self.ClassTimes.append(var)
            if y.split('-')[-1][-1] == ')':
                ub = y.split('-')[-1][:-1]
            else:
                ub = y.split('-')[-1]
            if ub not in self.ClassRoom:
                self.ClassRoom.append(ub)

            

    def __str__(self):
        return f'Course Code: {self.CourseCode}\nProgram: {self.Program}\nFaculty: {self.Faculty}\nCredits: {self.Credit}\nSection: {self.Section}\nDate, Time, Room: {self.DayTimeRoom}\nTotal Seat: {self.TotalSeat}\nSeat Booked: {self.SeatBooked}\nSeat Remaining: {self.SeatRemaining}'


holder = {f'{courses[0]}sec{courses[4]}': Course(courses) for courses in table[1:]}
# 
# print(holder['CSE111sec03'])
# print('Lab?: ', holder['CSE111sec03'].labExists)
# print(holder['CSE461sec01'].ClassTimes)

'''
GRID
------------------------------------------
|8:00-9:20      |9:30-10:50     |11-12:20   |12:30-1:50    |2-3:20   |3:30-4:50  |5-6:20|
Saturday | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 |
Sunday   | 1.0 | 1.1 | 1.2 | 1.3 | 1.4 | 1.5 | 1.6 |
Monday   | 2.0 | 2.1 | 2.2 | 2.3 | 2.4 | 2.5 | 2.6 |
Tuesday  | 3.0 | 3.1 | 3.2 | 3.3 | 3.4 | 3.5 | 3.6 |
Wednesday| 4.0 | 4.1 | 4.2 | 4.3 | 4.4 | 4.5 | 4.6 |
Thursday | 5.0 | 5.1 | 5.2 | 5.3 | 5.4 | 5.5 | 5.6 |
------------------------------------------
'''

class Routine:
    def __init__(self):
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.Saturday = self.board[0]
        self.Sunday = self.board[1]
        self.Monday = self.board[2]
        self.Tuesday = self.board[3]
        self.Wednesday = self.board[4]
        self.Thursday = self.board[5]
        self.courses = []

    def conflictChecker(self, courseCode):
        # if int(holder[f'{str(courseCode)}'].SeatRemaining) <= 0:
        #     return False
            # print(f'No seats remaining for {courseCode}')
        for eachDay in self.board:
        #     for x in eachDay:
        #         # print(x)
        #         if courseCode[:6] in str(x):
        #             return False
            if holder[courseCode].CourseCode in eachDay:
                return False
        for classTime in holder[str(courseCode)].ClassTimes:
            if int(classTime[0]) == 2:
                return False 
            # if int(classTime[0]) == 3:
                # return False 
            if int(classTime[0]) == 4:
                return False 
            if self.board[int(classTime[0])][int(classTime[2])] != 0:
                return False
        return True

    def addCourse(self, courseCode):
        self.courses.append(courseCode)
        for classTime in holder[courseCode].ClassTimes:
            self.board[int(classTime[0])][int(classTime[2])] = courseCode

                

    def generateRoutine(self):
        table = ['Day/Time', '8:00 - 9:20', '9:30 - 10:50', '11:00 - 12:20', '12:30 - 1:50', '2:00 - 3:20', '3:30 - 4:50', '5:00 - 6:20']
        days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        t = PrettyTable(table)
        for x in range(len(self.board)):
            self.board[x].insert(0, days[x])
        # # print('BOARD VALUES', self.board[0])
        # # print(self.board)
        # for x in range(len(self.board)):
        #     self.board[x].pop(0)
        t.add_rows(self.board)
        return t




inputs = ['CSE340', 'CSE350', 'CSE461', 'CSE331']
inputLen = len(inputs)

def checkSequence(sequence):
    for courseCode in sequence:
        if not board.conflictChecker(courseCode):
            return False
    return True
                    
    
# while True:
#     if len(board.courses) == len(inputs):
#         break
# for y in inputs:
#     p = any(y in sublist for sublist in board.board)
#     if not p:
#         courseTaker()
# board.generateRoutine()
# print(f'Courses Taken - {board.courses}')

# for x in courses if len(x)>0:
# courses = []
# #Taking all the keys 
# for x in holder.keys():
#     courses.append(x)
if __name__== "__main__":
    count = 0
    coursesGrp = [[] for x in range(inputLen)]
    # print(coursesGrp)
    for x in range(len(inputs)):
        for y in list(holder.keys()):
            if inputs[x] in y:
                coursesGrp[x].append(y)
    # print(courses)
    combinations = [x for x in itertools.product(*coursesGrp)]
    # print(combinations[:10])
    # print(combinations[0])
    with open('routines.txt', 'w') as f:
        for sequence in combinations:
            board = Routine()
            if checkSequence(sequence):
                for courseCode in sequence:
                    board.addCourse(courseCode)
                for eachCourse in board.courses:
                    f.writelines(f'{eachCourse} - {holder[eachCourse].Faculty} | ')
                f.write('\n')
                f.writelines(f'{board.generateRoutine()}\n \n \n')
                count+=1
    print(count)




app = Flask('__name__')

@app.route("/")
def hello_world():
    print(f'NOMAN')
    return "<p>Hello, World!</p>"
# create a post method that will take list of courses from the route
@app.route("/courses", methods=['POST'])

