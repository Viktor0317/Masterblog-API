from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data
POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post about Flask."},
    {"id": 2, "title": "Second Post", "content": "This is a tutorial on Python."},
    {"id": 3, "title": "Flask API", "content": "Learn how to build RESTful APIs with Flask."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Returns all blog posts with optional sorting"""
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc').lower()

    # Validate sorting field if provided
    valid_sort_fields = {"title", "content"}
    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field. Allowed values: {list(valid_sort_fields)}"}), 400

    # Validate direction if provided
    if direction not in {"asc", "desc"}:
        return jsonify({"error": "Invalid direction. Allowed values: 'asc', 'desc'"}), 400

    # Apply sorting if a valid sort field is provided
    sorted_posts = sorted(POSTS, key=lambda post: post[sort_field].lower(), reverse=(direction == "desc")) if sort_field else POSTS

    return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Handles adding a new post"""
    data = request.get_json()

    # Validate input
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Both 'title' and 'content' are required"}), 400

    # Generate a unique ID
    new_id = POSTS[-1]['id'] + 1 if POSTS else 1

    # Create new post object
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    # Add new post to the list
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Handles deleting a post by its ID"""
    global POSTS

    # Find the index of the post
    post_index = next((index for index, post in enumerate(POSTS) if post["id"] == post_id), None)

    if post_index is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    # Remove the post
    deleted_post = POSTS.pop(post_index)

    return jsonify({"message": f"Post with id {deleted_post['id']} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Handles updating an existing post"""
    data = request.get_json()

    # Find the post
    post = next((post for post in POSTS if post["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    # Update fields if provided, otherwise keep the old values
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search posts by title or content"""
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    # Filter posts based on search query
    matching_posts = [
        post for post in POSTS
        if (title_query and title_query in post["title"].lower()) or
           (content_query and content_query in post["content"].lower())
    ]

    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
