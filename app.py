from flask import Flask, jsonify, request

app = Flask(__name__)

# Имитация базы данных в памяти
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]


@app.route("/api/users", methods=["GET"])
def get_users():
  return jsonify(users), 200


@app.route("/api/users", methods=["POST"])
def create_user():
  data = request.get_json()
  if not data or "name" not in data:
    return jsonify({"error": "Name is required"}), 400

  new_user = {"id": len(users) + 1, "name": data["name"]}
  users.append(new_user)
  return jsonify(new_user), 201


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
  global users
  user = next((u for u in users if u["id"] == user_id), None)
  if not user:
    return jsonify({"error": "User not found"}), 404

  users = [u for u in users if u["id"] != user_id]
  return jsonify({"message": "User deleted successfully"}), 200


# Демонстрационная уязвимость для SAST (Bandit найдет B307: suspicious-eval-usage)
@app.route("/api/calculate", methods=["POST"])
def calculate():
  expression = request.json.get("expr", "")
  # Опасно! Eval используется специально для демонстрации срабатывания Bandit
  result = eval(expression)
  return jsonify({"result": result})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)