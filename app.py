from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

def load_posts():
    with open("blog_posts.json", "r") as file:
        blog_posts = json.load(file)

    return blog_posts
@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        blog_posts = load_posts()

        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1
        else:
            new_id = 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)

        with open("blog_posts.json", "w") as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add-post.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)