from flask import Flask, render_template_string, render_template, redirect, request, url_for
from block import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        creditor = request.form['creditor']
        amount = request.form['amount']
        borrower = request.form['borrower']
        
        block_added = blockchain.add_block(creditor, amount, borrower)
        if block_added == True:
            return redirect(url_for('index'))
        else:
            return render_template_string('<div>Failure</div>')

@app.route('/check', methods=['GET'])
def check():
    chain_blocks = blockchain.check_integrity()
    chain_is_corrupted = blockchain.has_corrupted_results(chain_blocks)
    return render_template('index.html', is_corrupted=chain_is_corrupted, chain_blocks=chain_blocks)

if __name__ == "__main__":
    app.run(debug=True, port=1984)
