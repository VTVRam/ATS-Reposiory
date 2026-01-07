import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from ai_engine import analyze_resume, mock_job_database
import logging

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Initialize App
app = Flask(__name__, static_folder='../', static_url_path='/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HireFlow')

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serves the main HireFlow HTML interface."""
    # Assuming hire_flow.html is in the parent directory or same directory
    # Adjust path as needed based on where you place this file relative to the HTML
    try:
        return send_file('hire_flow.html') 
    except FileNotFoundError:
        # Fallback if running from the same directory
        return send_file('../hire_flow.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_candidate():
    """
    Main Endpoint: Receives resume, parses it, and runs AI analysis.
    """
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            logger.info(f"Processing file: {filename}")
            
            # --- AI PROCESSING STEP ---
            # 1. Extract Text (Simulated here, but would use PyPDF2/python-docx)
            # 2. Analyze Content
            analysis_result = analyze_resume(filepath)
            
            # 3. Match Jobs
            matching_jobs = mock_job_database(analysis_result['skills'])
            
            # Construct Response
            response = {
                'candidate_profile': {
                    'name': "Candidate", # In real app, extract from text
                    'score': analysis_result['score'],
                    'summary': analysis_result['summary'],
                    'top_skills': analysis_result['skills']
                },
                'market_analysis': {
                    'demand_level': analysis_result['demand'],
                    'salary_range': analysis_result['salary_est']
                },
                'matches': matching_jobs
            }
            
            # Cleanup: Remove file after processing to save space
            os.remove(filepath)
            
            return jsonify(response)

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return jsonify({'error': 'Internal server error during processing'}), 500
    
    return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT'}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'active', 'system': 'HireFlow AI Core'})

if __name__ == '__main__':
    print("----------------------------------------------------------")
    print("HireFlow AI Engine Started")
    print("Access the platform at http://localhost:5000")
    print("----------------------------------------------------------")
    app.run(debug=True, port=5000)
