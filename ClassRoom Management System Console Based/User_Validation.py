#BCSF19A005
#BCSF19A037

import re


class InvalidMenuChoice(Exception):
    pass

class InvalidIDException(Exception):
    pass

class InvalidPostException(Exception):
    pass

class InvalidChoiceException(Exception):
    pass

class InvalidNameException(Exception):
    pass

class InvalidEmailException(Exception):
    pass

class InvalidPasswordException(Exception):
    pass

class InvalidDateException(Exception):
    pass



class UserValidation:
    def __init__(self):
        pass

    def checkUserchoice(self, ch, n):
        if ch <= 0 or ch > n:
            raise InvalidChoiceException("Exception Invalid Choice. ")

    def inputUserChoice(self, totalCh):
        flag = True
        while flag == True:
            try:
                if totalCh == 3:
                    choice = input("Enter your choice number (1,2,3) : ")
                else:
                    choice = input("Enter your choice number (1-2) : ")

                choice = int(choice)
                try:
                    self.checkUserchoice(choice, totalCh)
                except InvalidChoiceException as e:
                    raise InvalidChoiceException(e)
                flag = False
            except ValueError as e:
                print("Exception Occur Value Error : ", e)
            except InvalidChoiceException as e:
                print(f" Choice Number should e between(1-{totalCh})!!", e)
            except Exception as e:
                print(e)
        return choice

    def validateUserID(self, uId2):
        if len(uId2) <= 0:
            raise InvalidIDException("Exception Ocurr : ID is Invalid(length cannot be 0).")

    def inputID(self, str1):
        flag = False
        while flag == False:
            try:
                userID = input(str1)
                self.validateUserID(userID)
                flag = True
            except Exception as e:
                print(str(e))
        return userID

    def inputName(self, str1="Enter your Name : "):
        flag = False
        while flag == False:
            try:
                name = input(str1)
                self.validateName(name)
                flag = True
            except Exception as e:
                print(str(e))
        return name

    def checkIsDigit(self, str1):
        for ch in str1:
            if ch.isdigit() == True:
                return True
        return False

    def validateName(self, name1):
        if (self.checkIsDigit(name1) == True):
            raise InvalidNameException("Exception Occur!! : Name should not contain digits. ")
        if (len(name1) <= 0):
            raise InvalidNameException("Exception Occur!! : Name should not be empty. ")

    def validateEmail(self, email1):
        if (len(email1) <= 0):
            raise InvalidEmailException("Exception Occur!! : Email cannot not be empty. ")
        else:
            st = re.fullmatch(r'[a-zA-Z0-9._+]+@(yahoo.com|gmail.com|outlook.com)', email1)
            if st == None:
                raise InvalidEmailException("Exception Occur : Invlaid Email Format!!!")

    def validatePassword(self, pwd1, flagstatus=False):
        if flagstatus == True and len(pwd1) < 8:
            raise InvalidPasswordException("Exception Occur!! : Invalid Password. ")
        elif len(pwd1) < 8:
            raise InvalidPasswordException("Exception Occur!! : Password should contain atleast 8 characters. ")
