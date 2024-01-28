from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

# Route to run the Python script
@app.route('/run-python-script', methods=['POST'])
def run_python_script():
    try:
        # Run the main.py script in the 'script' directory
        subprocess.run(['python', 'script/main.py'])
        return 'Script executed successfully!', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
