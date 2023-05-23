#BCSF19A005
#BCSF19A037

import random
import re

from DBHandler import DataBaseHandler
from Classes import ClassObject
from Classes import EnrollmentObject
from Menu import Menu
from User_Validation import *

class Teacher_View(UserValidation):

    def __init__(self):
        self.menu1 = Menu()
        self.DBObj = DataBaseHandler("localhost", "root", '', "classroommanagementsystem")

    def generateClassId(self, unique):
        chars = "bdfhjlnprtvxz"
        str = ""
        value = ""

        for str in range(5):
            value = value + random.choice(chars)
        return value

    def createClassroom(self, id1):

        unique = set()
        classID = self.generateClassId(unique)
        IdList = self.DBObj.fetchIDs("Teacher", classID)
        if len(IdList) == 0:
            status = False
            while status == False:
                unique = set()
                Class_Id = self.generateClassId(unique)
                status = self.DBObj.checkClassID("Teacher", Class_Id)
                if status == True:
                    classroom1 = ClassObject()
                    classroom1.classId = Class_Id
                    classroom1.className = self.inputName("ENTER THE NAME OF THE CLASSROOM: ")
                    classroom1.TeacherId = id1
                    idList = str(id1).split("_")
                    classroom1.TeacherNo = idList[1]
                    self.DBObj.addClassroom(classroom1)
                else:
                    status = False
            print("Class Room Created Successfully!!")
        else:
            print("Class Room Already Exist!")

    def removeStudent(self):
        stdId1 = self.inputID("Enter Student ID which you want to remove :")
        classId = self.inputID("Enter Class ID from which you want to remove the Student :")

        status1 = self.DBObj.checkStudentEnrollment(stdId1)

        if status1 == False:
            print("No student Exist!!")
        else:
            status2 = self.DBObj.checkClassEnrollment(stdId1, classId)

            if (status1 == True and status2 == True):
                self.DBObj.removeStdFromClass(stdId1, classId)
            elif status2 == False:
                print("No such Class Exist!!")

    def validatePost(self, str2):
        words = len(re.findall(r'\w+', str2))
        if len(str2) <= 0:
            raise InvalidPostException("Exception Occur: Your Post Length is 0. ")
        elif words > 10:
            raise InvalidPostException("Exception Occur: Words Limit Exceed!!\nPost word limit is 100.")

    def inputPost(self, str1):
        flag = False
        while flag == False:
            try:
                postStr = input(str1)
                self.validatePost(postStr)
                flag = True
            except Exception as e:
                print(str(e))
        return postStr

    def createTeacherPost(self, teachId):
        classId = self.inputID("Enter Class ID in which you want to create Post : ")
        existSt = self.DBObj.checkClassexist(classId)
        if (existSt == True):
            postString = self.inputPost("Enter your post string : ")
            self.DBObj.createPost(classId, teachId, postString)
        else:
            print("Class Id does not Exist!!")

    def startTeacherMenu(self, id1):
        userInput = ""
        while userInput != 'q':
            self.menu1.displayTeacherMenu()
            userInput = self.menu1.inputMenuChoice(5)
            if userInput == 1:
                self.createClassroom(id1)


            elif userInput == 2:
                enrollment = EnrollmentObject()
                classID = self.inputID("Enter the Class id: ")
                status = self.DBObj.verifyId(classID, "Teacher", id1)
                if status == True:
                    enrollment.classId = classID
                    enrollment.TeacherId = id1
                    choice = 'y'
                    while choice == 'Y' or choice == 'y':
                        studId = input("Enter the Id of the student you want to add: ")
                        Stulist = self.DBObj.fetchStudents()
                        result1 = self.DBObj.verifyStudent(studId, Stulist)
                        if result1 == True:
                            res = self.DBObj.checkClassEnrollment(studId,classID)
                            if res == False:
                                enrollment.stuId = studId
                                idList = str(enrollment.stuId).split("_")
                                enrollment.stuNo = idList[1]
                                self.DBObj.addToClassroom(Stulist, enrollment)
                            else:
                                status=self.DBObj.enrollStatusStd(studId,classID)
                                if status==True:
                                    print("Student Already Exist!!!")
                        elif result1 == False:
                            print("Student does not exist ")
                        print("DO you want to enter another student press y/Y to continue or any key to exit. ")
                        choice = input()
                else:
                    print("Classroom Id does not exist")

            elif userInput == 3:
                self.removeStudent()

            elif userInput == 4:
                print("Your Class IDs are:")
                idlist = self.DBObj.fetchIDs("Teacher", id1)
                count = 1
                for i in idlist:
                    print(count, ": ", i[0])
                    count += 1
                classId1 = input("enter you class id from above: ")
                result = self.DBObj.verifyId(classId1, "Teacher", id1)
                if result == True:
                    print("From which category you want to search by:")
                    print("1. By Name")
                    print("2. By StudentID")
                    choice = self.inputUserChoice(2)
                    if choice == 1:
                        stuName = self.inputName("Enter the name of the student:")
                        status = self.DBObj.searchStudent(stuName, 1, classId1)
                        if status == True:
                            print("student founded in class id", classId1)
                        else:
                            print("student not found")
                    elif choice == 2:
                        studId = self.inputID("Enter the ID of student: ")
                        status = self.DBObj.verifyId(classId1, "Student", studId)
                        if status == True:
                            resultSearch = self.DBObj.searchStudent(studId, 2, classId1)
                            if resultSearch == True:
                                print("student founded in class id", classId1)
                            else:
                                print("student not found")
                        else:
                            print("student ID does not exist")
                else:
                    print("Class Id does not Exist!!!")


            elif userInput == 5:
                self.createTeacherPost(id1)


class Student_View(UserValidation):
    def __init__(self):
        self.menu2 = Menu()
        self.stdDb1 = DataBaseHandler("localhost", "root", '', "classroommanagementsystem")

    def joinClass(self, stdId1):
        classId = self.inputID("Enter ID of Class which you want to join :")
        status = self.stdDb1.checkClassexist(classId)
        list1 = []
        if status == True:
            enrollment1 = EnrollmentObject()
            enrollment1.classId = classId
            enrollment1.TeacherId = self.stdDb1.getTeacherId(classId)
            enrollment1.stuId = stdId1
            idList = str(stdId1).split("_")
            enrollment1.stuNo = idList[1]
            status = self.stdDb1.checkClassEnrollment(enrollment1.stuId, enrollment1.classId)

            if status == False:
                self.stdDb1.addToClassroom(list1, enrollment1)
            else:
                print("You Cannot Join Again!!")
        else:
            print("Class Not Exist!!")

    def viewPostTeacher(self, stdId):
        classId = self.inputID("Enter ID of Class to View its Class Posts :")
        status = self.stdDb1.checkClassexist(classId)
        if status == True:
            teacherId = self.stdDb1.getTeacherId(classId)
            status = self.stdDb1.checkClassEnrollment(stdId, classId, True)
            if status == True:
                self.stdDb1.displayPost(classId, teacherId)
            else:
                print("You are not Enrolled in Class!!")
        else:
            print("Class Not Exist!!")

    def leaveClassRoom(self, stdId1):
        classId = self.inputID("Enter ID of Class which you want to leave :")
        status = self.stdDb1.checkClassexist(classId)
        if status == True:
            st = self.stdDb1.checkClassEnrollment(stdId1, classId, True)
            if st == True:
                self.stdDb1.deleteStdFromClass(classId, stdId1)
            else:
                print("You are not Enrolled!!")
        else:
            print("Class Not Exist!!")

    def startStudentMenu(self, stdId):
        userInput = ""
        while userInput != 'q':
            self.menu2.displaystudentMenu()
            userInput = self.menu2.inputMenuChoice(3)

            if userInput == 1:
                self.joinClass(stdId)
            elif userInput == 2:
                self.leaveClassRoom(stdId)
            elif userInput == 3:
                self.viewPostTeacher(stdId)


class Admin_View(UserValidation):
    def __init__(self):
        self.menu3 = Menu()
        self.admDB = DataBaseHandler("localhost", "root", '', "classroommanagementsystem")

    def deleteClassRoom(self):
        classID = self.inputID("Enter ID of Class which you want to delete: ")
        status = self.admDB.checkClassexist(classID)

        if status == True:
            st = self.admDB.deleteClass(classID)
        else:
            print("Class Not Exist!!")

    def validtaeDate(self, date1):
        if len(date1) <= 0:
            raise InvalidDateException("Invalid Date Exception: Date Length cannot be 0!!")
        else:
            st = re.fullmatch(r'\d{4}\-(0[1-9]|1[0-2])\-(0[1-9]|[1-2][0-9]|3[0-1])', date1)
            if st == None:
                raise InvalidDateException("Exception Occur : Invalid Date Format!!!")

    def inputDate(self, str1):
        flag = False
        while flag == False:
            try:
                date1 = input(str1)
                self.validtaeDate(date1)
                flag = True
            except Exception as e:
                print(str(e))
        return date1

    def viewClassRoomInfo(self, admId):
        date1 = self.inputDate("Enter date1 in format YYYY-MM-DD : ")
        date2 = self.inputDate("Enter date2 in format YYYY-MM-DD : ")
        self.admDB.viewClassRooms(date1, date2)

    def startAdminMenu(self, adminId):
        userInput = ""
        while userInput != 'q':
            self.menu3.displayAdminMenu()
            userInput = self.menu3.inputMenuChoice(5)

            if userInput == 1:
                self.deleteClassRoom()

            elif userInput == 2:
                print("Select which account to want to enable/disable:")
                print("1. Teacher")
                print("2. Student")
                choice = self.menu3.inputMenuChoice(2)

                print("Select choice \n1. Enable Account\n2. Disable Account")
                ch1 = self.inputUserChoice(2)

                str2 = ""
                if ch1 == 1:
                    acSt = 1
                    str2 = "Enabled"
                elif ch1 == 2:
                    acSt = 0
                    str2 = "Disabled"

                if choice == 1:
                    str2 = "Enter the ID of the Teacher:"
                    t_Id = self.inputID(str2)
                    teachStatus = self.admDB.checkTeacherStdExist("teacher", t_Id)
                    if teachStatus == True:
                        status = self.admDB.getAccountStatus(t_Id, "Teacher", acSt)
                        if status == True:
                            print("Account Having Account Type Teacher with Id", t_Id,
                                  f" has been {str2} successfully!")
                        else:
                            if acSt == 1:
                                print("Account Already Enable")
                            elif acSt == 0:
                                print("Account Already Disable")
                    else:
                        print("Teacher Id Does not Exist!!")
                if choice == 2:
                    str2 = "Enter the ID of the Student: "
                    s_Id = self.inputID(str2)
                    st1 = self.admDB.checkTeacherStdExist("student", s_Id)
                    if st1 == True:
                        status = self.admDB.getAccountStatus(s_Id, "Student", acSt)
                        if status == True:
                            print("Account Having Account Type Student with Id", s_Id,
                                  f" has been {str2} successfully!")
                        else:
                            if acSt == 1:
                                print("Account Already Enable")
                            elif acSt == 0:
                                print("Account Already Disable")
                    else:
                        print("Student Id Doe not Exist!")

            elif userInput == 3:
                self.viewClassRoomInfo(adminId)

            elif userInput == 4:
                stuName = self.inputID("Enter a student Name:")
                self.validateName(stuName)
                classID1 = self.inputID("Enter Class Id 1: ")
                resultStatus1 = False
                resultStatus2 = False

                while resultStatus1 == False:
                    flag1 = self.admDB.checkClassexist(classID1)
                    if flag1 == True:
                        resultStatus1 = True
                    else:
                        print("CLASS ID DOES NOT EXIST!!! ")
                        classID1 = self.inputID("Enter Class Id 1: ")
                        flag1 = self.admDB.checkClassexist(classID1)
                        resultStatus1 = False

                classID2 = self.inputID("Enter Class Id 2: ")
                while resultStatus2 == False:
                    flag2 = self.admDB.checkClassexist(classID2)
                    if flag2 == True:
                        resultStatus2 = True
                    else:
                        print("CLASS ID DOES NOT EXIST!!! ")
                        classID1 = self.inputID("Enter Class Id 1: ")
                        flag2 = self.admDB.checkClassexist(classID2)
                        resultStatus2 = False
                data = self.admDB.searchStudentInClasses(stuName, classID1, classID2)
                if data:
                    print("The student having name ", stuName, " is found successfully.")
                    for i in range(len(data)):
                        print(f"Student ID : {data[i]}     ")
                else:
                    print("No student found")