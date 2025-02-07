"""
Masterblog API - A RESTful API for managing blog posts.

This API allows users to create, retrieve, update, and delete blog posts.
It also supports searching and sorting posts.

Author: Nikola Brajkovic
Date: 2025-02-07
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# Sample data
POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post about Flask."},
    {"id": 2, "title": "Second Post", "content": "This is a tutorial on Python."},
    {"id": 3, "title": "Flask API", "content": "Learn how to build RESTful APIs with Flask."},
]

# Swagger configuration
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Masterblog API"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all blog posts.

    Optional query parameters:
    - sort: Sort posts by 'title' or 'content'.
    - direction: Sort order, 'asc' (ascending) or 'desc' (descending).

    Returns:
        JSON response containing a list of posts.
    """
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc').lower()

    # Validate sorting field
    valid_sort_fields = {"title", "content"}
    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field. Allowed values: {list(valid_sort_fields)}"}), 400

    # Validate direction
    if direction not in {"asc", "desc"}:
        return jsonify({"error": "Invalid direction. Allowed values: 'asc', 'desc'"}), 400

    # Sort posts if valid sort field is provided
    sorted_posts = sorted(POSTS, key=lambda post: post[sort_field].lower(), reverse=(direction == "desc")) if sort_field else POSTS

    return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Create a new blog post.

    Request Body (JSON):
    {
        "title": "Post Title",
        "content": "Post Content"
    }

    Returns:
        JSON response containing the created post.
    """
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Both 'title' and 'content' are required"}), 400

    new_id = POSTS[-1]['id'] + 1 if POSTS else 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a blog post by its ID.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        JSON response confirming the deletion or an error message if not found.
    """
    global POSTS

    post_index = next((index for index, post in enumerate(POSTS) if post["id"] == post_id), None)

    if post_index is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    deleted_post = POSTS.pop(post_index)

    return jsonify({"message": f"Post with id {deleted_post['id']} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing blog post.

    Args:
        post_id (int): The ID of the post to update.

    Request Body (JSON):
    {
        "title": "Updated Title",
        "content": "Updated Content"
    }

    Returns:
        JSON response containing the updated post or an error message if not found.
    """
    data = request.get_json()

    post = next((post for post in POSTS if post["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for blog posts by title or content.

    Query Parameters:
    - title (str): Search term for the title.
    - content (str): Search term for the content.

    Returns:
        JSON response containing matching posts.
    """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    matching_posts = [
        post for post in POSTS
        if (title_query and title_query in post["title"].lower()) or
           (content_query and content_query in post["content"].lower())
    ]

    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
