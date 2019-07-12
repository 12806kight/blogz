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
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs, title='Build-a-blog')

    else:
        blog = Blog.query.get(blog_id)
        return render_template('post.html', blog=blog, title='Blog Post')


@app.route('/newblog', methods=['POST', 'GET'])
def newblog():
    blog_title = ""
    blog_body = ""
    title_error = ""
    body_error = ""
    new_blog = Blog(blog_title, blog_body)
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['input']
        if not blog_title:
            title_error = "Enter a title!!!"
        if not blog_body:
            body_error = "Enter a body!!!"
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('post.html',title="Blog", blog=new_blog)
    return render_template('newblog.html',title="Build A Blog", title_error=title_error, blog_error=body_error, blog_title=blog_title, blog_body=blog_body)
        

    

    
    
if __name__ == '__main__':
    app.run()