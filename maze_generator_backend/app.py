from flask import Flask, request, jsonify
from flask_cors import CORS
from build import Build

app = Flask(__name__)
CORS(app)

@app.route('/generate-maze', methods=['GET'])
def generate_maze():
	try:
		h = int(request.args.get('h', 10))
		w = int(request.args.get('w', 10))
		branch_weight = float(request.args.get('branch', 0.25))
		triple_branch_weight = float(request.args.get('triple', 0.25))

		maze = Build(h, w, branch_weight, triple_branch_weight)
		maze.grow_tree()
		data = maze.export_maze_cells()

		return jsonify({"maze": data})
	except Exception as e:
		return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
	import os
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', debug=True)