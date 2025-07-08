# app.py

from flask import Flask, render_template # 導入 render_template
from datetime import datetime # 導入 datetime 模組來獲取當前日期

app = Flask(__name__)

@app.route('/')
def hello_world():
    # 獲取當前日期
    today = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    # 渲染 index.html 模板，並將 today 變數傳遞給模板
    return render_template('index.html', current_date=today)

if __name__ == '__main__':
    app.run(debug=True)