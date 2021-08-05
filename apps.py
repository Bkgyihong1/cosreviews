from flask import Flask, render_template, url_for, redirect, request
from qforms import *
from utils import *


app = Flask(__name__)

app.config['SECRET_KEY'] = 'webirfp'


@app.route('/', methods=['GET', 'POST'])
def home():
    form = queryForm()
    if request.method == 'POST':
        query = request.form.get('query')
        serps, brand = bm25_scores(query)
        if not serps:
            return redirect(url_for('error'))
        return redirect(url_for('serp'))
    return render_template('home.html', form=form)


@app.route('/serp', methods=['POST', 'GET'])
def serp():
    form = queryForm()
    query = request.form.get('query')
    serps, brand = bm25_scores(query)
    print(serps)
    recc = related(query, brand)
    print(recc)
    if request.method == 'POST':
        if not serps:
            return redirect(url_for('error'))
        return render_template('serp.html', title='Results', recc=recc,  query=query, serps=serps, form=form)
    return redirect(request.referrer)


@app.route('/products')
def products():
    if request.method == 'POST':
        return redirect(url_for('serp'))
    return render_template('products.html', title='Products')


@app.route('/error')
def error():
    return render_template('error.html', title='Oops')


if __name__ == '__main__':
    app.run(debug=True)
