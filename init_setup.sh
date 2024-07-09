echo[$(date)] : "Setting up the project"

echo[$(date)] : "Creating the virtual environment with python version 3.11.5"

python3 -m venv creditfault

echo[$(date)] : "Activating the virtual environment"

source creditfault/bin/activate

echo[$(date)] : "Upgrading pip, setuptools and wheel"

pip install --upgrade pip setuptools wheel

echo[$(date)] : "Installing the required development packages"

pip install -r requirements_dev.txt

echo[$(date)] : "Project setup complete"

echo[$(date)] : "To activate the virtual environment, run 'source creditfault/bin/activate'"

echo[$(date)] : "To deactivate the virtual environment, run 'deactivate'"

echo[$(date)] : "To run the tests, run 'pytest'"    

echo[$(date)] : "To run the application, run 'python -m app.py'"
