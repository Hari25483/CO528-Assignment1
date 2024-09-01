from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask application instance
app = Flask(__name__)

# Configure the SQLite database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# Create a SQLAlchemy object
db = SQLAlchemy(app)

# Define the BlogPost model
class BlogPost(db.Model):
    # Define the columns of the BlogPost table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Method to convert the BlogPost object to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

# Route to get all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    # Query all blog posts from the database
    posts = BlogPost.query.all()
    # Return the list of posts as JSON
    return jsonify([post.to_dict() for post in posts])

# Route to create a new blog post
@app.route('/posts', methods=['POST'])
def create_post():
    # Parse the incoming JSON data
    data = request.json
    # Create a new BlogPost instance with the provided data
    new_post = BlogPost(title=data['title'], content=data['content'])
    # Add the new post to the session and commit to the database
    db.session.add(new_post)
    db.session.commit()
    # Return the newly created post as JSON with a 201 Created status code
    return jsonify(new_post.to_dict()), 201

# Route to get a specific blog post by its ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    # Query the database for the post with the given ID, or return 404 if not found
    post = BlogPost.query.get_or_404(post_id)
    # Return the post as JSON
    return jsonify(post.to_dict())

# Route to update an existing blog post by its ID
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    # Query the database for the post with the given ID, or return 404 if not found
    post = BlogPost.query.get_or_404(post_id)
    # Parse the incoming JSON data
    data = request.json
    # Update the post's title and content
    post.title = data['title']
    post.content = data['content']
    # Commit the changes to the database
    db.session.commit()
    # Return the updated post as JSON
    return jsonify(post.to_dict())

# Route to delete a specific blog post by its ID
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Query the database for the post with the given ID, or return 404 if not found
    post = BlogPost.query.get_or_404(post_id)
    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()
    # Return a 204 No Content status code to indicate successful deletion
    return '', 204

# Ensure the application context is created and the database is initialized
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Run the Flask application with debugging enabled, listening on all interfaces at port 5003
    app.run(debug=True, host='0.0.0.0', port=5003)