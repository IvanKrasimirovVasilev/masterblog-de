from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

def load_posts():
    with open("blog_posts.json", "r") as file:
        blog_posts = json.load(file)

    return blog_posts

def fetch_post_by_id(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post['id'] == post_id:
            return post

    return None

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
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    blog_posts = load_posts()

    post = None

    for blog_post in blog_posts:
        if blog_post['id'] == post_id:
            post = blog_post
            break

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        with open("blog_posts.json", "w") as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('update-post.html', post=post)
@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    with open("blog_posts.json", "w") as file:
        json.dump(blog_posts, file)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)