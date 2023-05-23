#BCSF19A005
#BCSF19A037

class InvalidMenuChoice(Exception):
    pass


class Menu:
    def __init__(self):
        pass

    def displayTeacherMenu(self):
        print("*********************************************************************************")
        print("\t\t\t\t\t\t\t\t\"-------------Teacher's VIEW-------------\"")
        print("Press q to quit from Classroom Management System.")
        print("*********************************************************************************")
        print("Select your choice")
        print("1. Create Classroom")
        print("2. Add Student to Classroom")
        print("3. Remove Student")
        print("4. Search Classroom")
        print("5. Create Post")
        print("*********************************************************************************")
        print("*********************************************************************************")

    def displaystudentMenu(self):
        print("*********************************************************************************")
        print("\t\t\t\t\t\t\t\t\"-------------Student VIEW-------------\"")
        print("Press q to quit from Classroom Management System.")
        print("*********************************************************************************")
        print("Select your choice")
        print("1. Join Class")
        print("2. Leave Class room")
        print("3. View Teachers Post")
        print("*********************************************************************************")
        print("*********************************************************************************")


    def displayAdminMenu(self):
        print("*********************************************************************************")
        print("\t\t\t\t\t\t\t\t\"-------------Admin VIEW-------------\"")
        print("Press q to quit from Classroom Management System.")
        print("*********************************************************************************")
        print("Select your choice")
        print("1. Delete Classrooms")
        print("2. Update user Info’s")
        print("3. Classroom Info")
        print("4. Search Students")
        print("*********************************************************************************")
        print("*********************************************************************************")


    def __validateMenuChoice(self,num,high):
        if num<=0 or num>high:
            raise InvalidMenuChoice("Exception: Invalid Menu Choice Number ")

    def inputMenuChoice(self,high):
        flag=True
        while flag == True:
            try:
                ch=input(f"Enter your Menu Choice (1-{high}) : ")
                if ch !='q':
                    ch=int(ch)
                    self.__validateMenuChoice(ch,high)
                flag=False
            except ValueError as e:
                print("Exception Value Error : ",e)
            except InvalidMenuChoice as e:
                print(e,f"Choice Number should e between(1-{high})!!")
            except Exception as e:
                print("Exception Occur",e)
        return ch
