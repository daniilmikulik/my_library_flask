from flask import Flask, render_template, jsonify, redirect, request
import json
import datetime

with open("./data/library.json", encoding='utf8') as jsonFile:
    library = json.load(jsonFile)
    jsonFile.close()

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('index.html', library=library)


@app.route("/book/<string:name>")
def book_page(name):
    book = None
    for item in library:
        if item["title"] == name:
            book = item
            break
    return render_template('book.html', book=book)


@app.route('/library/<string:filter_mode>')
def choose_filter(filter_mode):
    titles = []
    if filter_mode == 'in':
        for item in library:
            titles.append({"title": item["title"], "status": item["isInLibrary"]})
    elif filter_mode == 'return':
        for item in library:
            status = 'true'
            if item["dateGiven"] != "-" and item["isInLibrary"] == "false":
                status = "false"
            titles.append({"title": item["title"], "status": status})
    elif filter_mode == "expired":
        for item in library:
            status = 'true'
            if item["dateGiven"] == "-" and item["isInLibrary"] == "true":
                status = "false"
            titles.append({"title": item["title"], "status": status})
    return jsonify(titles)


@app.route('/edit/<string:mode>')
def edit_page(mode):
    return render_template('edit_form.html', mode=mode)


@app.route('/add', methods=['POST'])
def add_book():
    for item in library:
        if item["title"] == request.form["title"]:
            return redirect('/')

    library.append({
        "title": request.form["title"],
        "author": request.form["author"],
        "dateOfCreation": request.form["date"],
        "isInLibrary": "true",
        "dateGiven": "-",
        "dateOfReturn": "-",
        "keeperName": "-"
    })
    return redirect('/')


@app.route('/<string:mode>', methods=['POST'])
def edit_book(mode):
    for item in library:
        if item["title"] == mode:
            if request.form['title']:
                item["title"] = request.form['title']
            if request.form['author']:
                item["author"] = request.form['author']
            if request.form['date']:
                item["dateOfCreation"] = request.form['date']
    return redirect('/')


@app.route('/delete/<string:name>')
def delete_book(name):
    for item in library:
        if item['title'] == name:
            library.remove(item)
            return redirect('/')
    return redirect('/')


@app.route('/give/<string:name>', methods=['POST'])
def give_book(name):
    for item in library:
        if item['title'] == name:
            if request.form['name']:
                item["keeperName"] = request.form['name']
                item['dateGiven'] = str(datetime.datetime.now()).split()[0]
                item['dateOfReturn'] = request.form['dateOfReturn']
                item['isInLibrary'] = 'false'
                return redirect('/')
    return redirect('/')


@app.route('/return/<string:name>')
def return_book(name):
    for item in library:
        if item["title"] == name:
            item['keeperName'] = "-"
            item['dateGiven'] = "-"
            item['dateOfReturn'] = "-"
            item['isInLibrary'] = 'true'
            return redirect('/')
    return redirect('/')
