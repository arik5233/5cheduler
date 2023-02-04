from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
from ast import literal_eval
from prettytable import PrettyTable
import itertools
import threading

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
coursesHolder = [f'{courses[0]}' for courses in table[1:]]
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

    def __str__(self) -> str:
        return f'{self.Saturday}\n{self.Sunday}\n{self.Monday}\n{self.Tuesday}\n{self.Wednesday}\n{self.Thursday}'

    def conflictChecker(self, courseCode, days, times, faculties):
        # if int(holder[f'{str(courseCode)}'].SeatRemaining) <= 0:
        #     return False
        def checkFaculty(self, courseCode, faculties):
            if holder[courseCode].Faculty not in faculties:
                return False
            return True

        # def checkDay(self, classTime, day):
        #     if int(classTime[0]) != int(day):
        #         return False
        #     return True
        
        # def checkTime(self, classTime, time):
        #     if int(classTime[2]) != int(time):
        #         return False
        #     return True

        # def courseExists(self, courseCode, eachDay):
        #     if holder[courseCode].CourseCode not in eachDay:
        #         return False
        #     return True

        def freeSlot(self, classTime):
            if self.board[int(classTime[0])][int(classTime[2])] == 0:
                return True
            else:
                return False

        # for eachDay in self.board:
        #     checkAlreadyExists = courseExists(self, courseCode, eachDay)
        #     if not checkAlreadyExists:
        #         continue
        #     else:
        #         return True

        for classTime in holder[str(courseCode)].ClassTimes:

            if classTime[0] not in days or classTime[2] not in times:
                return False
                
            freePos = freeSlot(self, classTime)
            if not freePos:
                return False

        facultyCheck = checkFaculty(self, courseCode, faculties)
        
        if facultyCheck:
            return True
        else:
            return False


    def checkSequence(self, sequence, days, times, allCourseFaculties):
        for x in range(len(sequence)):
            if not self.conflictChecker(sequence[x], days, times, allCourseFaculties[x]):
                return False
            else:
                self.addCourse(sequence[x])
        return True
    
    def getFaculty(self, courseCode):
        faculties = []
        for x in holder.keys():
            if courseCode in x:
                faculties.append(holder[x].Faculty)
        return faculties

    def addCourse(self, courseCode):
        self.courses.append(courseCode)
        for classTime in holder[courseCode].ClassTimes:
            self.board[int(classTime[0])][int(classTime[2])] = courseCode[:6]

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
        return t, self.board
                    
def makeCombination(inputs):
    coursesGrp = [[] for x in range(len(inputs))]
    # print(coursesGrp)
    for x in range(len(inputs)):
        for y in list(holder.keys()):
            if inputs[x] in y:
                coursesGrp[x].append(y)
    # print(courses)
    combinations = [x for x in itertools.product(*coursesGrp)]
    return combinations


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
# if __name__== "__main__":
    # count = 0
    # coursesGrp = [[] for x in range(inputLen)]
    # # print(coursesGrp)
    # for x in range(len(inputs)):
    #     for y in list(holder.keys()):
    #         if inputs[x] in y:
    #             coursesGrp[x].append(y)
    # # print(courses)
    # combinations = [x for x in itertools.product(*coursesGrp)]
    # print(combinations[:10])
    # print(combinations[0])
    # with open('routines.txt', 'w') as f:
    #     for sequence in combinations:
    #         board = Routine()
    #         if checkSequence(sequence):
    #             for courseCode in sequence:
    #                 board.addCourse(courseCode)
    #             for eachCourse in board.courses:
    #                 f.writelines(f'{eachCourse} - {holder[eachCourse].Faculty} | ')
    #             f.write('\n')
    #             f.writelines(f'{board.generateRoutine()}\n \n \n')
    #             count+=1
    # print(count)

def getFaculty(courseCode):
        faculties = []
        for x in holder.keys():
            if courseCode in x:
                faculties.append(holder[x].Faculty)
        return faculties



def makeCombination(inputs):
    coursesGrp = [[] for x in range(len(inputs))]
    # print(coursesGrp)
    for x in range(len(inputs)):
        for y in list(holder.keys()):
            if inputs[x] in y:
                coursesGrp[x].append(y)
    # print(courses)
    combinations = [x for x in itertools.product(*coursesGrp)]
    return combinations

app = Flask('__name__', template_folder='templates', static_folder='static')


def makeRoutines():
    global allCourseFaculties, times, days, combinations
    allCourseFaculties = []
    times = request.form.getlist('time')
    days = request.form.getlist('day')
    # print(days)
    for x in range(1, no+1):
        faculties = request.form.getlist(f'checkboxFaculty{x}')
        # print(faculties)
        allCourseFaculties.append(faculties)
    # print(no, courses, times, days, allCourseFaculties)
    # print(allCourseFaculties)
    combinations = makeCombination(courses)
    routines = []
    # arr = []
    count = 0
    for sequence in combinations:
        board = Routine()
        checked = board.checkSequence(sequence, days, times, allCourseFaculties)
        if checked:    
            temp = ''
            for eachCourse in board.courses:
                temp += f'{eachCourse[:6]}({eachCourse[9:]})-{holder[eachCourse].Faculty}  |  '
            table, routineBoard = board.generateRoutine()
            html_table = table.get_html_string()
            routines.append((temp, html_table))
            # arr.append(temp)
            # print(f'{temp}\n \n')
            count+=1
    # print(routines)
        else:
            continue
    return (count, routines)


@app.route('/', methods=['GET'])
def home():
    # global count
    # count = request.form.get('count')
    return render_template('index.html')

@app.route('/routines', methods=['POST'])
def routines():
    # count, routines = None, None
    # start calculation in a separate thread
    thread = threading.Thread(target=makeRoutines)
    thread.start()
    thread.join()
    # return render_template('routines.html', value=)
    count, routines = makeRoutines()

        # print(count)
    if count == 0:
        return render_template('noroutines.html')
    else:
        return render_template('routines.html', value=routines)
    
@app.route('/process_input', methods=['POST'])
def process_input():
    global no, courses
    allFaculties = []
    coursesRand = request.json['courses']
    courses = [str(x).upper() for x in coursesRand]
    no = int(request.json['no'])
    for course in courses:
        allFaculties.append(getFaculty(course))
    for x in range(len(allFaculties)):
        allFaculties[x] = sorted(list(set(allFaculties[x])))
    # print(allFaculties)
    return allFaculties

  
if __name__ == '__main__':
    app.run(debug=True)

# gunicorn -w 4 -b 127.0.0.1:4000 app:app
    # return redirect('routines.html', value=routines)
