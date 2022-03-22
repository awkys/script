import os
import time

import pymysql

# def findAllFile(base):
#     for root, ds, fs in os.walk(base):
#         for f in fs:
#             yield f
def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname

def getSignUser():
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='123456',
                         database='sspanel')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = """SELECT email
       FROM `user`
       where class_expire < date(now())"""

    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()

    user = []
    for i in results:
        user.append(i[0])

    return user

def main():
    base = "../data"

    userAll = []  #所有用户
    signAndAll = [] #老用户已注册
    unsign = [] #老用户未注册
    signUser = getSignUser()
    for i in findAllFile(base):
        txt = open(i, encoding='gb18030', errors='ignore')
        for user in txt.readlines():
            email = user[:-1]
            if email not in [userAll]:
                userAll.append(email)

                if email in signUser:
                    signAndAll.append(email)
                else:
                    unsign.append(email)

    userAll = list(set(userAll))

    # allOldUser = []
    # for i in set(userAll):
    #     allOldUser.append(i+"\n")
    #
    # f = open("../data/allOldUser.txt", "w")
    # f.writelines(set(allOldUser))
    # f.close()

    unSignUser = []
    for i in set(unsign):
        unSignUser.append(i + "\n")

    f = open("../data/unSignUser.txt", "w")
    f.writelines(set(unSignUser))
    f.close()

    print("老用户总量：" + str(len(set(userAll))) + " - " + str(set(userAll)))
    print("已注册用户总量：" + str(len(set(signUser))) + " - " + str(set(signUser)))
    print("老用户已注册总量：" + str(len(set(signAndAll))) + " - " + str(set(signAndAll)))
    print("老用户未注册：" + str(len(set(unsign))) + " - " + str(set(unsign)))

if __name__ == '__main__':
    main()
