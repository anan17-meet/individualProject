from flask import Flask ,flash, render_template , request , redirect, url_for
from databases import *

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"


engine = create_engine('sqlite:///Dishes.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

@app.route("/")
def showAllDishes():
	allDishes = session.query(Dish).all()
	return render_template("mainpage.html",allDishes = allDishes)



@app.route("/recipes")
def recipes():
	return render_template('recipes.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

#@app.route('/dish')
#def dishes():
#	items = session.query(Dish).all()
#	return render_template("dishes.html",items = items)
@app.route("/dish/<int:dish_id>/")
def dishes(dish_id):
	item = session.query(Dish).filter_by(id=dish_id).one()
	return render_template('dishes.html', item=item)

@app.route("/addNewDish", methods = ['GET','POST'])
def addANewDish():
	if request.method == 'GET':
		return render_template("newdish.html")
	elif request.method == 'POST':
		name=request.form['name']
		instructions = request.form['instructions']
		picture = request.form['photo']
		ingredients = request.form['ingredients']
		newDish = Dish(name = name , picture = picture  ,instructions= instructions , ingredients = ingredients)
		session.add(newDish)
		session.commit()
		return redirect(url_for('showAllDishes'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email is None or password is None:
			flash('Missing Arguments')
			return redirect(url_for('login'))
		if verify_password(email, password):
			customer = session.query(Customer).filter_by(email=email).one()
			flash('Login Successful, welcome, %s' % customer.name)
			
			return redirect(url_for('showAllDishes'))
		else:
			# incorrect username/password
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))


@app.route('/newuser', methods = ['GET','POST'])
def newCustomer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        country = request.form['country']
        if name is None or email is None or password is None:
            flash("Your form is missing arguments")
            return redirect(url_for('newCustomer'))
        if session.query(Customer).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('newCustomer'))
        customer = Customer(name = name, email=email, country = country)
        customer.hash_password(password)
        session.add(customer)
        session.commit()
            
        
        return redirect(url_for('showAllDishes'))
        
    else:
        return render_template('newCustomer.html')

def verify_password(email, password):
	customer = session.query(Customer).filter_by(email=email).first()
	if not customer or not customer.verify_password(password):
		return False
	return True





if __name__=="__main__":
	app.debug = True
	app.run(port=8080)



