# go_commend_line
 
### 指令列生成器
源自於進行某些專案開發過程，可能需要重複下執行不同參數下的指令  
透過使用nicegui([ex4nicegui](https://github.com/CrystalWindSnake/ex4nicegui)擴展包)+結合資料庫儲存的方式，可以隨時攜帶下過的指令包隨時取用  
發想來自nicegui官方的"ToDoList" 做改寫


### 功能說明
- 新增項目可即時勾選使否使用
- 自定義新增參數名稱項目
- 一鍵複製組組合後的指令
- 指定類別儲存於資料庫

### 特色說明
- 借助 ex4nicegui 簡化原生 nicegui 的複雜綁定事件宣告
- 使用 sqlite3 做儲存


### 運行
```
python main.py
```
