#BCSF19A005
#BCSF19A037

from datetime import date

from Classes import *
import pymysql

class DataBaseHandler:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.con = None

        try:
            self.con = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database)
        except Exception as e:
            print("There is error in connection", str(e))

    def __del__(self):
        if self.con != None:
            self.con.close()

    def checkEmailexist(self,email1,accType):
        try:
            if self.con!=None:
                cur = self.con.cursor()
                if accType=="Teacher":
                    query1="select * from teacher where teacher_email=%s;"
                else:
                    query1="select * from student where student_email=%s;"
                args = (email1)
                cur.execute(query1, args)
                rows=cur.fetchall()
                cur.close()
                if(len(rows)==0):
                    return True
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def checkClassexist(self,classId):
        try:
            if self.con!=None:
                cur = self.con.cursor()
                query1="select * from classroom where classroom_id=%s and cls_remove_status=1;"
                args = (classId)
                cur.execute(query1, args)
                rows=cur.fetchall()
                cur.close()
                if(len(rows)>0):
                    return True
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def checkStudentEnrollment(self,id1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from student where student_id=%s and std_acc_status=1;"
                args = (id1)
                cur.execute(query1, args)
                rows = cur.fetchall()
                if (len(rows) >0):
                    query1 = "select * from enrollment where student_id=%s and enroll_status=1;"
                    args = (id1)
                    cur.execute(query1, args)
                    rows1 = cur.fetchall()
                    if(len(rows1)>0):
                        return True
                    else:
                        return False
                else:
                    return False
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def checkClassEnrollment(self,stdId1,classId1,flag1=False):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from classroom where classroom_id=%s and cls_remove_status=1;"
                args = (classId1)
                cur.execute(query1, args)
                rows = cur.fetchall()
                if (len(rows) >0):
                    if flag1==False:
                        query1 = "select * from enrollment where (student_id=%s and classroom_id=%s);"
                    else:
                        query1="select * from enrollment where (student_id=%s and classroom_id=%s) and enroll_status=1;"
                    args = (stdId1, classId1)
                    cur.execute(query1, args)
                    rows1 = cur.fetchall()
                    if len(rows1) > 0:
                        return True
                    else:
                        return False
                else:
                    return False
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def removeStdFromClass(self,stdId,classId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "update enrollment set enroll_status=0 where student_id=%s and classroom_id=%s;"
                args = (stdId, classId)
                cur.execute(query1, args)
                self.con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def enrollStatusStd(self,stdId,classId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1="select * from enrollment where (student_id=%s and classroom_id=%s) and enroll_status=1;"
                args = (stdId, classId)
                cur.execute(query1, args)
                rows1 = cur.fetchall()
                if len(rows1) > 0:
                    return True
                else:
                    query1 = "update enrollment set enroll_status=1 where student_id=%s and classroom_id=%s;"
                    args = (stdId, classId)
                    cur.execute(query1, args)
                    self.con.commit()
                    return False
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def deleteStdFromClass(self,classId,stdId1):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "delete from enrollment where student_id=%s and classroom_id=%s;"
                args = (stdId1, classId)
                cur.execute(query1, args)
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def checkUserAccountDisable(self,user2):
        try:

            if self.con!=None:
                cur = self.con.cursor()
                if user2.acc_type!="Admin":
                    if user2.acc_type=="Teacher":
                        query1="select * from teacher where teacher_email=%s and teacher_password=%s and tch_acc_status=0;"
                    elif user2.acc_type=="Student":
                        query1="select * from student where student_email=%s and student_password=%s and std_acc_status=0;"
                    args = (user2.email,user2.password)
                    cur.execute(query1, args)
                    rows=cur.fetchall()
                    if(len(rows)>0):
                        return True
                    else:
                        return False
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def checkUserExist(self,user2):
        try:
            if self.con != None:
                cur = self.con.cursor()
                if user2.acc_type == "Teacher":
                    query1 = "select * from teacher where teacher_email=%s and teacher_password=%s and tch_acc_status=1;"
                elif user2.acc_type == "Admin":
                    query1 = "select * from admin where admin_email=%s and admin_password=%s;"
                else:
                    query1 = "select * from student where student_email=%s and student_password=%s and std_acc_status=1;"
                args = (user2.email, user2.password)
                cur.execute(query1, args)
                rows = cur.fetchall()
                if (len(rows) > 0):
                    return True
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def disableAccount(self,user):
        try:
            if self.con!=None:
                cur = self.con.cursor()
                if user.acc_type=="Teacher":
                    query1="update teacher set tch_acc_status=0 where teacher_email=%s;"
                elif user.acc_type=="Student":
                    print("disable student")
                    query1="update student set std_acc_status=0 where student_email=%s;"
                else:
                    query1 = "update admin set std_acc_status=0 where admin_email=%s;"

            args = (user.email)
            cur.execute(query1, args)
            self.con.commit()
            rows=cur.fetchall()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()



    def addUser(self,user2):
        try:
            if self.con!=None:
                cur = self.con.cursor()
                if user2.acc_type=="Teacher":
                    query1="Insert into teacher(teacher_name,teacher_email,teacher_password) values(%s,%s,%s);"
                else:
                    query1 = "INSERT INTO student(student_name,student_email,student_password) values(%s,%s,%s);"

                args = (user2.name,user2.email,user2.password)
                cur.execute(query1, args)
                self.con.commit()

                if user2.acc_type=="Teacher":
                    query2="update teacher set teacher_id=concat(teacher_str,teacher_no);"
                else:
                    query2 = "update student set student_id=concat(student_str,student_no);"

                cur.execute(query2)
                self.con.commit()

                if user2.acc_type=="Teacher":
                    query3="select teacher_id from teacher where teacher_email=%s;"
                else:
                    query3 = "select student_id from student where student_email = %s;"

                args = (user2.email)
                cur.execute(query3,args)
                self.con.commit()
                return cur.fetchall()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def fetchIDs(self,acc_type,Id):
        try:
            if self.con != None:
                cur=self.con.cursor()
            if acc_type == "Teacher":
                query1 = "select classroom_id from classroom where teacher_id =%s and cls_remove_status=1"
                args=(Id)
                cur.execute(query1,args)
                IdList = cur.fetchall()
                return IdList

            elif acc_type=="Student":
                query1 = "select student_id from student where student_id =%s and std_acc_status=1"
                args=(Id)
                cur.execute(query1, args)
                IdList = cur.fetchall()
                return IdList
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def checkClassID(self, acc_type, ClassId):
        try:
            if self.con != None:
                cur = self.con.cursor()
            if acc_type == "Teacher":
                query1 = "select *  from  classroom where classroom_id=%s"
                args = (ClassId)
                cur.execute(query1, args)
                IdList = cur.fetchall()
                if len(IdList) == 0:
                    return True
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def getId(self,user):
        try:
            if self.con != None:
                cur=self.con.cursor()
            if user.acc_type == "Teacher":
                query1 = "select teacher_id from Teacher where teacher_email=%s"
            elif user.acc_type=="Student":
                query1 = "select student_id from student where student_email=%s"
            else:
                query1 = "select admin_id from admin where admin_email=%s"
            args=(user.email)
            cur.execute(query1,args)
            id = cur.fetchall()
            return id[0][0]

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def getTeacherId(self, classId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select teacher_id from classroom where classroom_id=%s and cls_remove_status=1"
                args = (classId)
                cur.execute(query1, args)
                id = cur.fetchall()
                return id[0][0]

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def addToClassroom(self, stuList=[], enroll=EnrollmentObject()):
        if len(stuList)==0:
            try:
                if self.con != None:
                    cur = self.con.cursor()
                    query1 = "insert into enrollment (classroom_id,student_id, student_no, teacher_id) values(%s,%s,%s,%s);"
                    args = (enroll.classId, enroll.stuId, int(enroll.stuNo), enroll.TeacherId)
                    cur.execute(query1, args)
                    self.con.commit()
            except Exception as e:
                print(str(e))
            finally:
                if cur != None:
                    cur.close()

        else:
            for i in stuList:
                if enroll.stuId in i[0]:
                    try:
                        if self.con != None:
                            cur = self.con.cursor()
                            query1 = "insert into enrollment (classroom_id,student_id, student_no, teacher_id) values(%s,%s,%s,%s);"
                            args = (enroll.classId, enroll.stuId, int(enroll.stuNo), enroll.TeacherId)
                            cur.execute(query1, args)
                            self.con.commit()
                    except Exception as e:
                        print(str(e))
                    finally:
                        if cur != None:
                            cur.close()

    def addClassroom(self,classObj1):
        try:
            if self.con != None:
                cur=self.con.cursor()
                query1 = "insert into classroom (classroom_name,classroom_id,teacher_no,teacher_id) values(%s,%s,%s,%s);"
                args=(classObj1.className,classObj1.classId,int(classObj1.TeacherNo),classObj1.TeacherId)
                cur.execute(query1,args)
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()


    def createPost(self,classId,teachID,postStr):
        try:
            if self.con != None:
                cur=self.con.cursor()
                query1 = "insert into post (classroom_id,teacher_id,post_string) values(%s,%s,%s);"
                args=(classId,teachID,postStr)
                cur.execute(query1,args)
                self.con.commit()

                query2 = "update post set post_id=concat(post_str,post_no);"
                cur.execute(query2)
                self.con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def displayPost(self,classId1,techId):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from post where classroom_id=%s and teacher_id=%s;"
                args = (classId1,techId)
                cur.execute(query1, args)
                postList = cur.fetchall()
                count=1;
                for str1 in postList:
                    print("POST ",count,". ",str1[5])
                    count=count+1

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def fetchStudents(self):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select student_Id from Student where std_acc_status=1"
                cur.execute(query1)
                result = cur.fetchall()
                return result

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def verifyStudent(self, stuID, StuList):
        for i in StuList:
            if stuID in i[0]:
                return True
        return False

    def verifyId(self, classId, acc_type, id):
        if acc_type == "Teacher":
            idList = self.fetchIDs(acc_type, id)
            for i in range(0,len(idList)):
                if classId == idList[i][0]:
                    return True
            return False
        elif acc_type == "Student":
            idList = self.fetchIDs(acc_type, id)
            for i in idList:
                if id == i[0]:
                    return True
            return False

    def searchStudent(self, toSearch, choice, cId):
        if choice == 1:
            try:
                if self.con != None:
                    cur = self.con.cursor()
                    query1 = "select student_id from enrollment where classroom_id=%s and enroll_status=1 "
                    args = (cId)
                    cur.execute(query1, args)
                    searchList = cur.fetchall()
                    query2 = "select student_id from student where student_name=%s and std_acc_status=1"
                    args = (toSearch)
                    cur.execute(query2, args)
                    stuId = cur.fetchall()
                    if len(searchList)>0:
                        for i in searchList:
                            if stuId[0][0] == i[0]:
                                return True
                    return False

            except Exception as e:
                print(str(e))
            finally:
                if cur != None:
                    cur.close()
        elif choice == 2:
            try:
                if self.con != None:
                    cur = self.con.cursor()
                    query1 = "select student_id from enrollment where classroom_id=%s and enroll_status=1"
                    args = (cId)
                    cur.execute(query1, args)
                    result = cur.fetchall()

                    if len(result) == 0:
                        return False
                    else:
                        return True

            except Exception as e:
                print(str(e))
            finally:
                if cur != None:
                    cur.close()

    def deleteClass(self,classID):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "delete from enrollment where classroom_id=%s;"
                args = (classID)
                cur.execute(query1, args)
                self.con.commit()

                query1 = "delete from post where classroom_id=%s;"
                args = (classID)
                cur.execute(query1, args)
                self.con.commit()


                query1 = "update classroom set cls_remove_status=0 where classroom_id=%s;"
                args = (classID)
                cur.execute(query1,args)
                self.con.commit()

                d2 = date.today().strftime("%Y-%m-%d")
                query1 = "update classroom set date_deleted =%s where classroom_id=%s;"
                args = (str(d2),classID)
                cur.execute(query1, args)
                self.con.commit()

                print("updated and deleted Successfully!!")

        except Exception as e:
            print("Exceprion Ocuur : ",str(e))
        finally:
            if cur != None:
                cur.close()

    def  viewClassRooms(self,date1,date2):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select * from classroom where date_created BETWEEN %s and %s"
                args = (str(date1),str(date2))
                cur.execute(query1, args)
                count1 = len(cur.fetchall())

                query1 = "select * from classroom where date_deleted BETWEEN %s and %s"
                args = (str(date1),str(date2))
                cur.execute(query1, args)
                count2 = len(cur.fetchall())

                print("**********CLASSROOM INFORMATION**********")
                print(f"Classrooms created between {date1} and {date2} is : {count1}")
                print(f"Classrooms deleted between {date1} and {date2} is : {count2}")


        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def getAccountStatus(self, id, acc_type,accStatus):
        try:
            if self.con != None:
                cur = self.con.cursor()
                if acc_type == "Teacher":
                    query1 = "select tch_acc_status from teacher where teacher_id=%s"
                if acc_type == "Student":
                    query1 = "select std_acc_status from student where student_id=%s"

                args = (id)
                cur.execute(query1, args)
                status = cur.fetchall()
                if len(status)>0:
                    if status[0][0]==accStatus:
                        return False

                if acc_type == "Teacher":
                    query2 = "update teacher set tch_acc_status=%s where teacher_id=%s;"
                if acc_type == "Student":
                    query2 = "update student set std_acc_status=%s where student_id=%s"

                args = (accStatus,id)
                cur.execute(query2, args)
                self.con.commit()
                return True

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def searchStudentInClasses(self, stuName, c_Id1, c_Id2):
        try:
            if self.con != None:
                cur = self.con.cursor()
                query1 = "select student_id from student where student_name=%s"
                args = (stuName)
                cur.execute(query1, args)
                studentID = cur.fetchall()
                std_ID = studentID
                result = []
                for i in range(len(std_ID)):
                    query2 = "select student_id from enrollment where student_id=%s and (classroom_id=%s or classroom_id=%s)"
                    args = (std_ID[i][0], c_Id1, c_Id2)
                    cur.execute(query2, args)
                    result1 = cur.fetchall()
                    if len(result1)>0:
                        result.append(result1[0][0])
                return result
        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()

    def checkTeacherStdExist(self,accType,Id):
        try:
            if self.con != None:
                cur = self.con.cursor()
                if accType=="teacher":
                    query1 = "select * from teacher where teacher_id=%s;"
                if accType == "student":
                    query1 = "select * from student where student_id=%s;"
                args = (Id)
                cur.execute(query1, args)
                rows = cur.fetchall()
                if (len(rows) > 0):
                    return True
                else:
                    return False

        except Exception as e:
            print(str(e))
        finally:
            if cur != None:
                cur.close()