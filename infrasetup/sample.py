import psycopg2

name = input("Please enter the name of the user:")
print name

def IdFind(name):
        con = None
        try:
                con = psycopg2.connect("host='127.0.0.1' dbname='test' user='binod' password='binod'")
                cur = con.cursor()
                cur.execute("SELECT id FROM auth_user WHERE username='"+name+"'")
                x = cur.fetchall()
                print x
                con.commit()

        finally:
                if con:
                        con.close()

idfind = IdFind(name)

def CreateTable():
        con = None
        try:
                con = psycopg2.connect("host='127.0.0.1' dbname='test' user='binod' password='binod'")
                cur = con.cursor()
                cur.execute("CREATE TABLE test0(ClusterName VARCHAR(30),Region VARCHAR(20),Master VARCHAR(30),Masterno INT,InstaTypeM VARCHAR(20),Slave VARCHAR(30),SlaveNo INT,InstaTypeS VARCHAR(20),MasterASG VARCHAR(30),SlaveASG VARCHAR(30))")
                cur.execute("ALTER TABLE test0 ADD COLUMN id INT REFERENCES auth_user (id)")
                cur.execute("INSERT INTO test0 VALUES('Cluster1','Mumbai','Master1',2,'t2.medium','Slave1',4,'t2.micro','MasterASG1','SlaveASG1',1)")
                cur.execute("INSERT INTO test0 VALUES('Cluster2','Mumbai','Master2',2,'t2.medium','Slave2',6,'t2.micro','MasterASG2','SlaveASG2',1)")
                cur.execute("INSERT INTO test0 VALUES('Cluster3','Mumbai','Master3',3,'t2.medium','Slave3',8,'t2.micro','MasterASG3','SlaveASG3',1)")
                con.commit()

        finally:
                if con:
                        con.close()


createtable = CreateTable()

def InsertRow():
        con = None
        try:
                con = psycopg2.connect("host='127.0.0.1' dbname='test' user='binod' password='binod'")
                cur = con.cursor()
                cur.execute("INSERT INTO test0( ClusterName, Region, Master, Masterno, InstaTypeM, Slave, SlaveNo, InstaTypeS, MasterASG, SlaveASG, id) VALUES('Cluster4','Mumbai','Master4',3,'t2.medium','Slave4',10,'t2.micro','MasterASG4','SlaveASG4',1)")
                con.commit()

        finally:
                if con:
                        con.close()

insertrow = InsertRow()

def DeleteRow():
        con = None;
        try:
                con = psycopg2.connect("host='127.0.0.1' dbname='test' user='binod' password='binod'")
                cur = con.cursor()
                cur.execute("DELETE FROM test0 WHERE ClusterName = 'Cluster3'")
                con.commit()

        finally:
                if con:
                        con.close()

deleterow = DeleteRow()

def DetailsofRowF():
        con = None;
        try:
                con = psycopg2.connect("host='127.0.0.1' dbname='test' user='binod' password='binod'")
                cur = con.cursor()
                cur.execute("SELECT * FROM test0 WHERE ClusterName = 'Cluster1'")
                x = cur.fetchall()
                print x

        finally:
                if con:
                        con.close()

detailsofarowf = DetailsofRowF()

def DetailsofRowP():
        con = None;
        try:
                con = psycopg2.connect("host='127.0.0.1' dbname='test' user='binod' password='binod'")
                cur = con.cursor()
                cur.execute("SELECT MasterASG,SlaveASG FROM test0 WHERE ClusterName = 'Cluster1'")
                x = cur.fetchall()
                print x
        finally:
                if con:
                        con.close()

detailsofarowp = DetailsofRowP()

