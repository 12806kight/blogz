from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:holiday12806@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/')
        else:
            # explain why the login failed
            pass
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        username_error = ''
        password_error = ''
        verify_error=''

        if len(username) < 3 or len(username) > 20:
            username_error = 'Username should be inbetween 2 to 30 letters'
            username = ''

        if ' ' in username:
            username_error = 'Username error'
            username = ''

        if ' ' in password:
            password_error = 'Password Error'
            password = ''


        if len(password) < 3 or len(password) > 20:
            password_error = 'Password should be inbetween 2 to 30 letters'
            password = ''

        if verify != password:
            verify_error = 'Passwords must match'
            verify = ''
        if not username_error and not password_error and not verify_error:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/')
            else:
                return "Duplicate User"
        return render_template('signup.html', ue=username_error, password_error=password_error, username=username, password=password, verify=verify, verify_error=verify_error)
    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():
    owner = User.query.filter_by(username=session['username']).first()

    user_id = request.args.get('id')

    if user_id == None:
        user = User.query.all()
        return render_template('index.html', user=user, title='Build-a-blog')

    else:
        users = User.query.get(user_id)
        return render_template('user.html', users=users, title='Blogs' )


@app.route('/user', methods=['POST', 'GET'])
def user():
    user_id = request.args.get('id')
    blogs = Blog.query.filter_by(owner_id=user_id)
    return render_template('user.html', blogs=blogs,  title='Blogs' )




    

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('user.id')

    if blog_id == None:
        
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs, user_id=user_id, title='Build-a-blog')

    else:
        blog = Blog.query.get(blog_id)
        
        return render_template('post.html', blog=blog, user_id=user_id, title='Blog Post')


@app.route('/newblog', methods=['POST', 'GET'])
def newblog():
    blog_title = ""
    blog_body = ""
    title_error = ""
    body_error = ""
    owner = User.query.filter_by(username=session['username']).first()
    # new_blog = Blog(blog_title, blog_body, owner)
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['input']
        
        if not blog_title:
            title_error = "Enter a title!!!"
        if not blog_body:
            body_error = "Enter a body!!!"
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body, owner)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('post.html',title="Blog", blog=new_blog)
    return render_template('newblog.html',title="Build A Blog", title_error=title_error, blog_error=body_error, blog_title=blog_title, blog_body=blog_body)
    
if __name__ == '__main__':
    app.run()