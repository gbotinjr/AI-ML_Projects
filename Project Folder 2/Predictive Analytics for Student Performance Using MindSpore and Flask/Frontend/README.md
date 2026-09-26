Instructions: Running the Student Performance System (Partial Build)
Current Status: v0.5 (Interface + Model Integration Testing)
Last Updated: February 16, 2026


1. Verify Directory Structure
Before running anything, ensure your folder looks exactly like this so Python can find the files:

Plaintext
/Student_Project

    ├── app.py                
    ├── train_model.py         
    ├── student-mat.csv        
    ├── templates/
    │   ├── login.html
    │   └── dashboard.html
    └── static/
        └── style.css

        
2. Environment Setup
Open your terminal (Command Prompt or VS Code Terminal) and navigate to the project folder.

Step A: Create a Virtual Environment (Optional but Recommended)

Windows: python -m venv venv then venv\Scripts\activate

Mac/Linux: python3 -m venv venv then source venv/bin/activate

Step B: Install Required Libraries
Copy and paste this command to install all necessary tools at once:

Bash
pip install flask pandas numpy scikit-learn


3. Launch the Web Interface (The "Front End")
Now that the model file exists, we can start your Flask server.

Run the application:

Bash
python app.py
Watch the terminal:
You should see output similar to:

Plaintext
* Running on http://127.0.0.1:5000
* Debug mode: on

  
4. Test the Application
Open your web browser (Chrome, Edge, etc.).

Type in the address: http://127.0.0.1:5000/

Test the Flow:

Login: Enter any username/password (unless you coded specific ones, just press Login).

Dashboard: Try entering values (e.g., G1: 12, G2: 13, Absences: 2).

Predict: Click the "Predict" button.
