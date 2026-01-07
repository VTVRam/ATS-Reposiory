from flask import Flask, send_file
import os

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def home():
    """
    Route to serve the portfolio website.
    It looks for 'index.html' in the current directory.
    """
    # Get the absolute path to the index.html file to ensure it's found
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    
    try:
        return send_file(file_path)
    except FileNotFoundError:
        return "Error: index.html not found. Please ensure the file exists in the same directory as app.py.", 404

if __name__ == '__main__':
    # Run the app in debug mode
    print("---------------------------------------------------------")
    print("Server is running! Open http://localhost:5000 in your browser")
    print("---------------------------------------------------------")
    app.run(debug=True, port=5000)