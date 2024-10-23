from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert


# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} 

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # value = Column(String(100))  # 用來儲存指令的
    # category = Column(String(20))

class Commend(Base):
    __tablename__ = 'commend'
    __table_args__ = {'extend_existing': True} 

    # 表的结构:
    id = Column(Integer, primary_key=True,autoincrement=True)
    source_name = Column(String(20))
    value = Column(String(100))

# 初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
# engine = create_engine('sqlite:///test.db')
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)

# Base.metadata.create_all(engine)

# session = DBSession()
# session.add(User(id=5,name='test'))
# # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
# user = session.query(User).filter(User.id=='5').one()
# # 打印类型和对象的name属性:
# print('type:', type(user))
# print('name:', user.name)
# # 关闭Session:
# session.close()


class database_opertor:
    def __init__(self) -> None:
        # pass

        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        

    # 創建相關的資料庫
    # def create_table(self):

    #     Base.metadata.create_all(self.engine)  # 包含裡面所存在資料表

    def insert(self,item):
        session = self.DBSession()
        session.add(item)
        session.commit()
        session.close()



if __name__=='__main__':

    d_operator = database_opertor()

    c_item = Commend(source_name='test',value='ttest')
    d_operator.insert(c_item)


    

    