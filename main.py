from typing import List
from ex4nicegui import rxui,to_ref, bi
from itertools import count
from nicegui import ui
from nicegui import Tailwind, ui
import pyperclip
import pandas as pd
from database_go import *

ui.add_head_html('<link href="https://fonts.googleapis.com/css2?family=Material+Icons" rel="stylesheet">')



## 定義文字 css 樣式
title_classes = 'font-sans underline text-lg font-bold'

## 參數名與其值 結構定義
class pair_param(rxui.ViewModel):
    name=''
    value=''
    selected = True

    def __init__(self,name:str,value:str='',selected: bool=True):
        super().__init__()
        self.name = name
        self.value = value
        self.selected = selected



class commend_list(rxui.ViewModel):
    # title:str
    comList:List[pair_param] = []
    
    def __init__(self):
        super().__init__()

    def delete(self,item:pair_param):
        self.comList.remove(item)

    def add(self,name:str,value:str=''):
        self.comList.append(pair_param(name,value))

    @rxui.cached_var
    def display_commend(self):
        # final_commend = to_ref("")  # 黨定雙向零組件
        # print(f'作為最後喜善的commend line:{final_commend.value}')
        
        final_c = to_ref('')

        new_final_commend =''
        for idx,item in enumerate(cList.comList):
            if item.selected:
                if idx!=0:
                    new_final_commend+=' --'+item.name+' '+item.value
                else:
                    new_final_commend+=item.name+' '

        final_c.value = new_final_commend
        
        return final_c.value

# 顯示資料庫用的
d_opter = database_opertor()  # database create, init
cs_result = None

cbox_search = to_ref(False)
cbox_save = to_ref(False)

# show db search result, and ui refresh
@ui.refreshable
def show_search_result_ui(table_name,cat=''):
    cs_result =  d_opter.search(table_name,cat)
    print(f'跑進更新環節,cs:{cs_result}')
    if cs_result!=None:
        with ui.column():
            for rr in cs_result:
                with ui.row():
                    ui.label(rr.id).classes('mt-2')
                    ui.code(rr.value).classes('w-60')
                    ui.label(rr.category).classes('mt-2')
                    ui.label(rr.descript).classes('mt-2')



# custom set category save to database
'''儲存到自己想要的類別'''
def save_cate_to_database_ui():
    with ui.card().bind_visibility_from(cbox_save,'value').classes('w-200'):
        # ui.label(f'會被存入的value').tailwind.font_weight('extrabold').text_color('orange-400').\
        #         font_size('2xl').text_underline_offset('2px')
        ui.label('存入類別').classes(title_classes)
        rxui.label(lambda: f' {cList.display_commend.value}')

        save_cat_input = ui.input(label='category')  # 輸入要儲存的類別

        rxui.button('save',on_click=lambda:save_commend_to_database(cList.display_commend.value, save_cat_input.value) )
        save_cat_input.set_value('')


# handcraft function: copy to clipboard and notify
def copy_and_notify(label_):
    pyperclip.copy(label_)
    ui.notify('Copy the commend')


def main_controll_ui():   # 主控台 section
    with ui.card().classes('w-200'):

        rxui.label('Command generator').classes(title_classes)
        
        @rxui.vfor(cList.comList)  # for 迴圈 list
        def _(store:rxui.VforStore[pair_param]):
            p_item = store.get_item()
            

            with ui.row().classes('justify-center'):
                rxui.checkbox(value=p_item.selected).classes('w-10').classes('justify-center m-auto')
                rxui.input(value=p_item.name,placeholder='參數名',on_change=lambda:cList.display_commend).classes('w-20')
                rxui.input(value=p_item.value,placeholder='值',on_change=lambda:cList.display_commend).classes('w-60')
                btn_delete = ui.button(icon='delete').classes('justify-center mt-3')
                btn_delete.on_click(lambda: cList.delete(p_item))


        # add_item = rxui.input(value='', placeholder='參數名')
        with ui.row():
            # ui.label().classes('justify-center m-auto')
            add_item = ui.input(label='新增參數(enter)', placeholder='參數名')

            # 事件處理
        add_item.on('keydown.enter',lambda : (cList.add(add_item.value,'')))
        add_item.on('keydown.enter',lambda : add_item.set_value(' '))
        # add_item.on('keydown.enter',lambda : )


        rxui.label('完整的commend line')
        label_now = rxui.label(lambda: f"{cList.display_commend.value}").style('background: #C0C0C0; padding:5px')
        with ui.row():
            rxui.button('copy',on_click=lambda: copy_and_notify(label_now.text)) 
            # rxui.button('save',)
            ui.checkbox('save detail',value=False).bind_value(cbox_save,'value')
            ui.checkbox('Search',value=False).bind_value(cbox_search,'value')
            
            # cbox_save.value = save_



def search_result_ui():
    with ui.card().bind_visibility_from(cbox_search,'value'):  # 搜尋資料庫的 section
        ui.label('搜尋').classes(title_classes)
        list_table_name =  [key for key in table_dict.keys()]
        

        # d_opter.search_all_category()
        
        def update_cat_list(choose_table:str,cat_select):

            if len(choose_table)!=0:
                ref_cat_list.value = d_opter.search_all_category(choose_table[0])  # 更新類別列表
                cat_select.set_options(ref_cat_list.value)
            else:
                cat_select.set_options([])

        with ui.row():
            # ui.label('選擇資料表')
            select_table = ui.select(list_table_name, multiple=True, label='選擇資料表') \
                .classes('w-64').props('use-chips')
            

            ## 許則資料表下的屬性
            select_cat = ui.select(ref_cat_list.value, multiple=False, label='選擇類型') \
                .classes('w-64').props('use-chips')
            
            select_table.on_value_change(lambda:update_cat_list(select_table.value,select_cat))
            # select_cat.set_value(ref_cat_list)


        rxui.button('search',on_click = lambda: show_search_result_ui.refresh(select_table.value[0],select_cat.value))
        show_search_result_ui(cs_result)   # refresh search ui section


#commend list
cList = commend_list()
cList.add('python')


##  search section global ref
ref_cat_list = to_ref([])



with ui.row():
    
    main_controll_ui()  # 主要控制 ui


    with ui.grid():
        save_cate_to_database_ui()  # 將產生的 command 儲存到指定類別
        search_result_ui()
        # 用作搜尋資料庫的


def save_commend_to_database(value,category):
    c_item = Command(value=value,category=category,descript='')
    d_opter.insert_sepcify(c_item)
    ui.notify('Sussece save to database')
    # save_cat_input.set_value('')


ui.run(native=True,title='GO command line')

    
