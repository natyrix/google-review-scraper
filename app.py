from flask import *
import os,sys

sys.path.append(os.path.abspath(os.path.join("./scripts/")))

app = Flask(__name__, static_folder='staticFiles') 



@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        return render_template('home.html', title='Google review scrapper', error_text='')
    except Exception as e:
        return render_template('home.html', title='Google review scrapper', error_text=str(e))


if __name__ == '__main__':  
   app.run(debug = True) 