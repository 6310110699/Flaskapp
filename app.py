from flask import Flask, render_template, request, redirect, url_for
import pickle, uuid, os

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    try:
        with open('static/menu.txt', 'rb') as h:
            items = pickle.load(h)
    except:
        items = []
    
    if request.method == 'POST':
        form = request.form
        img = request.files['file']
        name = form['name']
        ingre = form['ingre']
        howto = form['howto']
        img_path = os.path.join('static/images', img.filename)
        img.save(img_path)

        item = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "ingre": ingre,
                    "howto": howto,
                    "img": img_path
                }
        items.append(item)
        with open('static/menu.txt', 'wb') as h:
            pickle.dump(items, h)
        group_items = [items[i:i+3] for i in range(0, len(items),3)]
    else:
        group_items = [items[i:i+3] for i in range(0, len(items),3)]

    return render_template('index.html', items = group_items)

@app.route('/delete',methods=['POST'])
def delete():
    with open('static/menu.txt', 'rb') as h:
        items = pickle.load(h)
    if request.method == 'POST':
        selected_items = request.form.getlist('multiitems')
        for i in selected_items:
            item = eval(i)
            items.remove(item)
        with open('static/menu.txt', 'wb') as h:
            pickle.dump(items, h)
        
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug = True)
