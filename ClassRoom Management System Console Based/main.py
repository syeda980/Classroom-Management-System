#BCSF19A005
#BCSF19A037

from DBHandler import DataBaseHandler
from Classes import *
from Interfaces import *

class UserNotExistException(Exception):
    pass


class LoginSignup(UserValidation):
    def __init__(self):
        self.stdDB = DataBaseHandler("localhost", "root", '', "classroommanagementsystem")
        super().__init__()


    def checkEmailDuplicate(self,email2,acType2):
        status = self.stdDB.checkEmailexist(email2, acType2)
        if status == False:
            raise InvalidEmailException("Exception Occur: Email Already Exist!!")

    def inputEmail(self,acType,loginStatus=False):
        flag=False
        while flag==False:
            try:
                email1 = input("Enter your Email : ")
                self.validateEmail(email1)
                if loginStatus==False:
                    self.checkEmailDuplicate(email1,acType)
                flag=True
            except Exception as e:
                print(str(e))
        return email1

    def inputPassword(self,loginStatus=False,user1=User()):
        flag = False
        count=0
        while flag == False:
            try:
                pwd = input("Enter your Password : ")
                count = count + 1
                self.validatePassword(pwd,loginStatus)
                flag = True


            except InvalidPasswordException as e:
                if count>3 and loginStatus==True:
                    print("More than 3 Wrong Attempts!!\nNow You Account is Disabled!! ")
                    self.stdDB.disableAccount(user1)
                    exit()
                print(str(e))
            except Exception as e:
                print(str(e))
        return pwd

    def checkLoginStatusAcc(self,user1):
        status = self.stdDB.checkUserAccountDisable(user1)
        flag = True

        if status == True:
            raise UserNotExistException("Exception Ocuur: Your Account is Disable")
            flag = False
        else:
            status1 = self.stdDB.checkUserExist(user1)
            if status1 == False:
                raise UserNotExistException("Exception Ocuur: User Not Exist")
        return flag


    def loginSignUpAccount(self):
        print("****************WELCOME TO CLASSROOM MANAGEMENT SYSTEM****************")
        print("Select your choice")
        print("1. SignUp")
        print("2. Login")
        choice1 = self.inputUserChoice(2)

        if(choice1==1):
            print("Types of account you can create \n1. Teacher\n2. Student ")
            print("Select Type of account")
            accChoice = self.inputUserChoice(2)
            if accChoice == 1:
                accountType = "Teacher"
                print("Teacher Account ")
            elif accChoice == 2:
                accountType = "Student"
                print("Student Account")

            name = self.inputName()
            email=self.inputEmail(accountType)
            password=self.inputPassword()

            user1=User(name,email,password,accountType)

            stdID=self.stdDB.addUser(user1);
            print("Your ID is : ",stdID[0][0])

        elif choice1==2:
            print("Types of Accounts \n1. Teacher\n2. Student\n3. Admin ")
            print("Select Type of account")
            accChoice = self.inputUserChoice(3)
            if accChoice == 1:
                accountType = "Teacher"
            elif accChoice == 2:
                accountType = "Student"
            elif accChoice == 3:
                accountType = "Admin"

            flag=False
            while flag==False:
                try:
                    email1 = self.inputEmail(accountType, True)
                    user2 = User("", email1, "", accountType)

                    password1 = self.inputPassword(True,user2)
                    user2.password=password1
                    st=self.checkLoginStatusAcc(user2)

                    flag=True
                    if (st == False):
                        exit()
                except Exception as e:
                    print("EXP : ",str(e))

            print("WELCOME You Are Login As ",user2.acc_type)
            id=self.stdDB.getId(user2)
            if user2.acc_type=="Teacher":
                teacher1=Teacher_View()
                teacher1.startTeacherMenu(id)
            if user2.acc_type=="Student":
                student1=Student_View()
                student1.startStudentMenu(id)
            if user2.acc_type == "Admin":
                admin1=Admin_View()
                admin1.startAdminMenu(id)




lg=LoginSignup()
lg.loginSignUpAccount()
