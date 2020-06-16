from flask import Flask,render_template,request
from engine.app import code_run,fullColorList
app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('./sudokuhome.html')

@app.route('/sudoku',methods=['POST','GET'])
def sudoku():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        boardSize = int(data.get('boardSize'))


        code_return = code_run(boardSize)
        print(code_return)
        color_pallete = fullColorList
        color_pallete.append('')
        return render_template('./sudokuexe.html',newmatrix =code_return,color_pallete=color_pallete)
    else:
        return 'something went wrong'


