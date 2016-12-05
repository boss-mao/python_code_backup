import pymssql
from datetime import datetime
from uuid import uuid1
reload(sys)
sys.setdefaultencoding('utf-8')

class SqlHelper:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise (NameError, u"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, u"连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql, parameters):
        cur = self.__GetConnect()
        cur.execute(sql, parameters)
        self.conn.commit()
        self.conn.close()


# 采用参数化的形式插入数据
sql_db = SqlHelper('192.168.1.6', 'Lvhe', 'Lvhe!Q@W#E$R', 'Lawyer')
sql = u"insert into tb_Contract(CID,ContractMenuId,Title,Content,CreateTime,Url,IsReserve,DownloadCount) values(%s,%s,%s,%s,%s,%s,%d,%d) "
parameters = (str(uuid1()).replace("-", ""),
              u'05504978-3dba-42aa-919c-001a6aef64e9',
              '你好'.decode('utf-8'),
              "哇哈哈".decode('utf-8'),
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "http://www.baidu.com".decode('utf-8'),
              0,
              0)
sql_db.ExecNonQuery(sql, parameters)
