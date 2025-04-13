from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.getImage import get_blog_image


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(3), nullable=False)
    subtitle = db.Column(db.String(3), nullable=False)
    author = db.Column(db.String(3), nullable=False)
    image_url = db.Column(db.String())
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)

    def __repr__(self) -> str:
        return f"{self.title} - {self.author}"


@app.route("/")
def hello_world():
    allBlogs = Blog.query.all()
    return render_template("index.html", current_page="home", allBlogs=allBlogs)

@app.route("/about")
def about():
    return render_template("about.html", current_page="about")

@app.route("/blog/<int:id>")
def viewBlog(id):
    blog = Blog.query.filter_by(id=id).first()
    return render_template("blogViewer.html", blog=blog)

@app.route("/blog/edit/<int:id>", methods=["GET", "POST"])
def editBlog(id):
    if request.method == 'POST':
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        author = request.form["author"]
        content = request.form["content"]

        image_url = get_blog_image(title, subtitle, content)

        blog = Blog.query.filter_by(id=id).first()

        blog.title=title
        blog.subtitle=subtitle
        blog.author=author
        blog.content=content
        blog.image_url=image_url

        db.session.add(blog)
        db.session.commit()
        return redirect("/")

    blog = Blog.query.filter_by(id=id).first()
    return render_template("Editblog.html", blog=blog)

@app.route("/blog/delete/<int:id>")
def deleteBlog(id):
    blog = Blog.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        author = request.form["author"]
        content = request.form["content"]

        # Get appropriate image using utility function
        image_url = get_blog_image(title, subtitle, content)

        post = Blog(title=title, subtitle=subtitle, author=author, content=content, image_url=image_url)
        db.session.add(post)
        db.session.commit()
        return redirect("/")

    return render_template("addBlog.html", current_page="addBlog")


if __name__ == "__main__":
    app.run(debug=True, port=3000)
