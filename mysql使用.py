# -*- coding: utf-8 -*-
'''
@time: 2018/8/10 8:37
@author: Jack Luo
@file: mysql使用.py
'''
import pymysql

db=pymysql.connect(host='localhost',db='spiders',user='root',password='123456',port=3306)
cur=db.cursor()

cur.execute('select version()')
data=cur.fetchone()
print(data)
cur.execute('create database spiders default character set utf8')
cur.execute('create table if not exists students (id varchar(255) not null ,name varchar(255) not null ,age int not null ,primary key (id))')

data={'id':'20180711','name':'jackal','age':20180711}
table='students'
keys=','.join(data.keys())
values=','.join(['%s']*len(data))
sql='insert into {table}({keys}) values({values}) on duplicate key update '.format(table=table,keys=keys,values=values)
update=','.join(['{key}=%s'.format(key=key) for key in data])
sql+=update

try:
    if cur.execute(sql,tuple(data.values())*2):
        print('good')
        db.commit()
except:
    print('bad')
    db.rollback()

try:
    cur.execute('update students set age={} where name= {}'.format(18,'jackal'))
    db.commit()
    print('good')
except:
    db.rollback()
    print('bad')

table='students'
condition='age>20'
try:
    cur.execute('delete from {} where {}'.format(table,condition))
    db.commit()
except:
    db.rollback()

try:
    cur.execute('select * from students where age>= 20')
    print('count:',cur.rowcount)
    one=cur.fetchone()
    print('one:',one)
    results=cur.fetchall()
    print('results:',results)
    print('results type:',type(results))
    for row in results:
        print(row)
    row=cur.fetchone()
    while row:
        print('row:',row)
        row=cur.fetchone()
except:
    print('error')
db.close()
