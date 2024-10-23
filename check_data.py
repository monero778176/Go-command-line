from typing import List
from ex4nicegui import rxui,to_ref, bi
from itertools import count
from nicegui import ui
from nicegui import Tailwind, ui
import pyperclip
import pandas as pd


ui.add_head_html('<link href="https://fonts.googleapis.com/css2?family=Material+Icons" rel="stylesheet">')

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
                    new_final_commend+='--'+item.name+' '+item.value
                else:
                    new_final_commend+=item.name+' '

        final_c.value = new_final_commend
        
        return final_c.value


cList = commend_list()
cList.add('python')

with ui.card().classes('w-200'):

    rxui.label('commend generator')
    
    @rxui.vfor(cList.comList)  # for 迴圈 list
    def _(store:rxui.VforStore[pair_param]):
        p_item = store.get_item()
        

        with ui.row().classes('justify-center'):
            rxui.checkbox(value=p_item.selected).classes('w-10').classes('justify-center m-auto')
            rxui.input(value=p_item.name,placeholder='參數名',on_change=lambda:cList.display_commend).classes('w-20')
            rxui.input(value=p_item.value,placeholder='值',on_change=lambda:cList.display_commend).classes('w-80')


    # add_item = rxui.input(value='', placeholder='參數名')
    with ui.row():
        ui.label('新增參數(enter)').classes('justify-center m-auto')
        add_item = ui.input(value='', placeholder='參數名')

        # 事件處理
    add_item.on('keydown.enter',lambda : (cList.add(add_item.value,'')))
    add_item.on('keydown.enter',lambda : add_item.set_value(' '))
    # add_item.on('keydown.enter',lambda : )


    rxui.label('完整的commend line')
    with ui.row():
        label_now = rxui.label(lambda: f"{cList.display_commend.value}").style('background: #C0C0C0; padding:5px')

        rxui.button('copy',on_click=lambda: copy_and_notify(label_now.text)) 
        rxui.button('save',)
    


## 按鈕事件: 觸發複製當前結果的功能
def copy_and_notify(x):
    pyperclip.copy(x)
    ui.notify("Has copy commend")




data = pd.DataFrame({"name": ["f", "a", "c", "b"], "age": [1, 2, 3, 1]})
ds = bi.data_source(data)

ds.ui_table(
    columns=[
        {"label": "new colA", "field": "colA", "sortable": True},
    ]
)

ui.run()
