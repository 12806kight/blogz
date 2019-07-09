from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blag:holiday12806@localhost:8889/build-a-blag'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/')
def index():
    return redirect('/newblog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')

    if blog_id == None:
        posts = Blog.query.all()
        return render_template('blog.html', posts=posts, title='Build-a-blog')

    else:
        post = Blog.query.get(blog_id)
        return render_template('post.html', post=post, title='Blog Post')


@app.route('/newblog', methods=['POST', 'GET'])
def newblog():
    blog_title= ""
    blog_body= ""
    new_blog = Blog(blog_title, blog_body)
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return render_template('post.html',title="Build A Blog", post=new_blog)
    return render_template('newblog.html',title="Build A Blog", post=new_blog)
        

    

    
    
if __name__ == '__main__':
    app.run()