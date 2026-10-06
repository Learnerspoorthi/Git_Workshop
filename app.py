from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

# In-memory storage (resets when the server restarts)
todos = []
next_id = 1


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/api/todos", methods=["GET"])
def list_todos():
    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def add_todo():
    global next_id
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400
    todo = {"id": next_id, "text": text, "done": False}
    next_id += 1
    todos.append(todo)
    return jsonify(todo), 201


@app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
def toggle_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            return jsonify(todo)
    return jsonify({"error": "Not found"}), 404


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
