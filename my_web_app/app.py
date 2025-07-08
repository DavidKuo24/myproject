# app.py

from flask import Flask

# 建立一個 Flask 應用程式實例
app = Flask(__name__)

# 定義一個路由 (Route)
# 當使用者訪問網站的根目錄 (例如: http://127.0.0.1:5000/) 時，會執行這個函式
@app.route('/')
def hello_world():
    return 'Hello, World!'

# 啟動 Flask 應用程式
# 如果這個檔案是直接被執行的 (而不是被其他檔案導入的)，就執行 app.run()
if __name__ == '__main__':
    app.run(debug=True) # debug=True 會在程式碼修改時自動重載，方便開發
