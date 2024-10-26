from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert,delete


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
    value = Column(String(100))
    category = Column(String(20))
    descript = Column(String(50))

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
table_dict = {'commend':Commend,'user':User}

class database_opertor:
    def __init__(self) -> None:
        # pass

        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    # 創建相關的資料庫
    # def create_table(self):

    #     Base.metadata.create_all(self.engine)  # 包含裡面所存在資料表

    def search(self,table_name,cat_value:str=''):
        # cs = self.session.query(table_dict[table_name]).filter_by(category=cat_value).all()

        try:
            print(f'試著查找資料表:{table_name}')
            print(f'進入db search::{cat_value}')
            if cat_value!='':
                print(f'查詢資料表:{table_name} 搜尋類別:{cat_value}')
                cs = self.session.query(table_dict[table_name]).filter_by(category=cat_value).all()
                print(f'回傳cs:{cs}')
            else:
                print(f'不具有類別')
                cs = self.session.query(table_dict[table_name]).all()

        except:
            cs = None
            print(f'搜尋上出點事情')
        return cs

    def insert(self,item):
        session = self.DBSession()
        session.add(item)
        session.commit()
        session.close()

    def insert_sepcify(self,c_item):
        if c_item is not None:
            session = self.DBSession()
            # id,value,cat,des = c_item

            session.add(c_item)
            session.commit()
            session.close()
            print(f'成功儲存資料到資料庫')


    def delete(self,table_name:str,id:int):
        
        session = self.DBSession()
        
        delete_item = delete(table_dict[table_name]).where(table_dict[table_name].id==id)
        print(f'要刪除的項目:{delete_item}')
        session.delete(delete_item)
        session.commit()
        session.close()

    def drop_table(self):
        Base.metadata.drop_all(bind=self.engine, tables=[Commend.__table__])


if __name__=='__main__':

    d_operator = database_opertor()
    # d_operator.drop_table()
    c_item = Commend(value='test',category='ttest',descript='None temp')
    d_operator.insert(c_item)


    

    