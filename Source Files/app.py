from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///props.db'
db = SQLAlchemy(app)

# Define the Prop model
class Prop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pixelcount = db.Column(db.Integer, nullable=False)
    modeltype = db.Column(db.String(50), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Route to view props
@app.route('/')
def index():
    props = Prop.query.all()
    return render_template('index.html', props=props)

# Route to add a new prop
@app.route('/add_prop', methods=['GET', 'POST'])
def add_prop():
    if request.method == 'POST':
        name = request.form['name']
        pixelcount = int(request.form['pixelcount'])
        modeltype = request.form['modeltype']

        # Check if the model type is valid
        valid_model_types = ['Arches', 'Tree 360', 'Candy Canes', 'Circle', 'Icicles', 'Single Line', 'Star','Custom']
        if modeltype not in valid_model_types:
            return "Invalid model type. Please choose from: " + ", ".join(valid_model_types)

        # Check for uniqueness before inserting
        if Prop.query.filter_by(name=name, pixelcount=pixelcount, modeltype=modeltype).first() is not None:
            return "Name must be unique"

        new_prop = Prop(name=name, pixelcount=pixelcount, modeltype=modeltype)
        db.session.add(new_prop)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_prop.html')

# Route to update an existing prop
@app.route('/update_prop/<int:id>', methods=['GET', 'POST'])
def update_prop(id):
    prop = Prop.query.get(id)

    if request.method == 'POST':
        prop.name = request.form['name']
        prop.pixelcount = int(request.form['pixelcount'])
        prop.modeltype = request.form['modeltype']

        # Check if the model type is valid
        valid_model_types = ['Arches', 'Tree 360', 'Candy Canes', 'Circle', 'Icicles', 'Single Line', 'Star', 'Custom']
        if prop.modeltype not in valid_model_types:
            return "Invalid model type. Please choose from: " + ", ".join(valid_model_types)

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('update_prop.html', prop=prop)

# Route to delete a prop
@app.route('/delete_prop/<int:id>', methods=['GET', 'POST'])
def delete_prop(id):
    prop = Prop.query.get(id)

    if request.method == 'POST':
        db.session.delete(prop)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('delete_prop.html', prop=prop)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
