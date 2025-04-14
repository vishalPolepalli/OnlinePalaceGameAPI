This API powers the backend for an app allowing multiple people to play a game of Palace online. 

Instructions to run the server locally: 
  1. Clone the repo
  2. Navigate to projects main folder
  3. Set up a venv
  4. Install the python dependencies
  5. Run the FastAPI App
  6. Use Postman to test endpoints

Set up venv: 
  1. python3 -m venv myenv
  2. source myenv/bin/activate

Install Dependencies:
  1. pip install -r requirements.txt

Run the FastAPI App: 
  1. python -m uvicorn main:app --reload 
  
