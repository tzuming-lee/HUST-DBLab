import pymysql

def query(cursor):
    table = input("输入你想查询的表：")
    sql = "SELECT * FROM " + table
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)

def addStudent(cursor):
    try:
        Sno = input("请输入学号：")
        Sname = input("请输入姓名：")
        Ssex = input("请输入性别(男/女)：")
        Sage = int(input("请输入年龄："))
        Sdept = input("请输入所在系：")
        Scholarship = input("有无奖学金(是/否)：")
        sql = "INSERT INTO Student (Sno, Sname, Ssex, Sage, Sdept, Scholarship) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (Sno, Sname, Ssex, Sage, Sdept, Scholarship))
        print("学生添加成功！")
    except Exception as e:
        print("添加学生时出错：", e)

def updateStudent(cursor):
    try:
        Sno = input("请输入学号：")
        update_query = "UPDATE Student SET"
        update_values = []
        while True:
            choice = int(input("输入1-5分别修改姓名，性别，年龄，系别，奖学金，输入0退出："))
            if choice == 1:
                Sname = input("请输入姓名：")
                update_query += " Sname = %s,"
                update_values.append(Sname)
            elif choice == 2:
                Ssex = input("请输入性别(男/女)：")
                update_query += " Ssex = %s,"
                update_values.append(Ssex)
            elif choice == 3:
                Sage = int(input("请输入年龄："))
                update_query += " Sage = %s,"
                update_values.append(Sage)
            elif choice == 4:
                Sdept = input("请输入系别：")
                update_query += " Sdept = %s,"
                update_values.append(Sdept)
            elif choice == 5:
                Scholarship = input("请输入有无奖学金(是/否)：")
                update_query += " Scholarship = %s,"
                update_values.append(Scholarship)
            else:
                break
        if update_values:
            update_query = update_query.rstrip(',') + " WHERE Sno = %s"
            update_values.append(Sno)
            cursor.execute(update_query, tuple(update_values))
            print("学生信息更新成功！")
    except Exception as e:
        print("更新学生信息时出错：", e)

def addCourse(cursor):
    try:
        Cno = input("请输入课程号：")
        Cname = input("请输入课程名：")
        Cpno = input("请输入先修课（若无先修课，输入NULL）：")
        Ccredit = int(input("请输入学分："))
        sql = "INSERT INTO Course (Cno, Cname, Cpno, Ccredit) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (Cno, Cname, Cpno if Cpno != 'NULL' else None, Ccredit))
        print("课程添加成功！")
    except Exception as e:
        print("添加课程时出错：", e)

def updateCourse(cursor):
    try:
        Cno = input("请输入课程号：")
        update_query = "UPDATE Course SET"
        update_values = []
        while True:
            choice = int(input("输入1-3分别修改课程名，先修课，学分，输入0退出："))
            if choice == 1:
                Cname = input("请输入课程名：")
                update_query += " Cname = %s,"
                update_values.append(Cname)
            elif choice == 2:
                Cpno = input("请输入先修课：")
                update_query += " Cpno = %s,"
                update_values.append(Cpno if Cpno != 'NULL' else None)
            elif choice == 3:
                Ccredit = int(input("请输入学分："))
                update_query += " Ccredit = %s,"
                update_values.append(Ccredit)
            else:
                break
        if update_values:
            update_query = update_query.rstrip(',') + " WHERE Cno = %s"
            update_values.append(Cno)
            cursor.execute(update_query, tuple(update_values))
            print("课程信息更新成功！")
    except Exception as e:
        print("更新课程信息时出错：", e)

def deleteNoneCourse(cursor):
    try:
        cursor.execute("DELETE FROM Course WHERE Cno NOT IN (SELECT Cno FROM SC)")
        print("无选课的课程已删除！")
    except Exception as e:
        print("删除课程时出错：", e)

def addSC(cursor):
    try:
        Sno = input("请输入学号：")
        Cno = input("请输入课程号：")
        Grade = int(input("请输入成绩："))
        sql = "INSERT INTO SC (Sno, Cno, Grade) VALUES (%s, %s, %s)"
        cursor.execute(sql, (Sno, Cno, Grade))
        print("成绩录入成功！")
    except Exception as e:
        print("录入成绩时出错：", e)

def updateSC(cursor):
    try:
        Sno = input("请输入学号：")
        Cno = input("请输入课程号：")
        Grade = int(input("请输入成绩："))
        sql = "UPDATE SC SET Grade = %s WHERE Sno = %s AND Cno = %s"
        cursor.execute(sql, (Grade, Sno, Cno))
        print("成绩更新成功！")
    except Exception as e:
        print("更新成绩时出错：", e)

def queryDeptGrade(cursor):
    choice = input("输入1-5分别按系查询平均成绩，最好成绩，最差成绩，优秀率，不及格人数：")
    sql = ""
    if choice == '1':
        sql = "SELECT Sdept, AVG(Grade) AS 平均成绩 FROM Student JOIN SC ON Student.Sno = SC.Sno GROUP BY Sdept"
    elif choice == '2':
        sql = "SELECT Sdept, MAX(Grade) AS 最好成绩 FROM Student JOIN SC ON Student.Sno = SC.Sno GROUP BY Sdept"
    elif choice == '3':
        sql = "SELECT Sdept, MIN(Grade) AS 最差成绩 FROM Student JOIN SC ON Student.Sno = SC.Sno GROUP BY Sdept"
    elif choice == '4':
        sql = "SELECT Sdept, (COUNT(CASE WHEN Grade >= 85 THEN 1 END) / COUNT(*)) * 100 AS 优秀率 FROM Student JOIN SC ON Student.Sno = SC.Sno GROUP BY Sdept"
    elif choice == '5':
        sql = "SELECT Sdept, COUNT(*) AS 不及格人数 FROM Student JOIN SC ON Student.Sno = SC.Sno WHERE Grade < 60 GROUP BY Sdept"
    else:
        print("输入无效")
        return
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)

def queryStudentGroupGrade(cursor):
    sql = "SELECT S.Sdept, SC.Sno, S.Sname, C.Cname, SC.Grade FROM SC JOIN Student S ON SC.Sno = S.Sno JOIN Course C ON SC.Cno = C.Cno ORDER BY S.Sdept, SC.Grade DESC"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(f"{row[0]}系的学号为{row[1]}的{row[2]}同学，{row[3]}课程成绩为{row[4]}")

def queryStudentGrade(cursor):
    Sno = input("输入学号：")
    sql = "SELECT S.*, C.Cname FROM Student S JOIN SC ON S.Sno = SC.Sno JOIN Course C ON SC.Cno = C.Cno WHERE S.Sno = %s"
    cursor.execute(sql, (Sno,))
    result = cursor.fetchall()
    if result:
        student_info = result[0]
        print(f"学号为{student_info[0]}的同学姓名是：{student_info[1]}, 性别是：{student_info[2]}, 年龄是{student_info[3]}, 来自{student_info[4]}系, 奖学金情况是：{student_info[5]}")
        courses = [row[-1] for row in result]
        print("该同学选修了" + ', '.join(courses) + "课程")

def main():
    conn = pymysql.connect(host='localhost', port=3306,user='root', password='1255', database='s_t_u202312319', charset='utf8')
    cursor = conn.cursor()
    while True:
        print("""
        1. 添加学生
        2. 更新学生信息
        3. 添加课程
        4. 更新课程
        5. 录入成绩
        6. 更新成绩
        7. 查找各系成绩表现
        8. 按系显示成绩
        9. 按学号查找学生信息及选课情况
        0. 删除没选课的课程
        q. 退出
        """)
        choice = input("请输入选项：")
        if choice == '1':
            addStudent(cursor)
        elif choice == '2':
            updateStudent(cursor)
        elif choice == '3':
            addCourse(cursor)
        elif choice == '4':
            updateCourse(cursor)
        elif choice == '5':
            addSC(cursor)
        elif choice == '6':
            updateSC(cursor)
        elif choice == '7':
            queryDeptGrade(cursor)
        elif choice == '8':
            queryStudentGroupGrade(cursor)
        elif choice == '9':
            queryStudentGrade(cursor)
        elif choice == '0':
            deleteNoneCourse(cursor)
        elif choice == 'q':
            break
        else:
            print("请输入正确的选项")
        conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
