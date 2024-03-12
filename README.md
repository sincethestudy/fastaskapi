# FastaskAPI

Welcome to FastaskAPI, a FastAPI project designed to streamline task management. This project leverages the speed and simplicity of FastAPI to provide a robust backend solution for managing tasks efficiently.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sincethestudy/fastaskapi.git
cd fastaskapi
```


2. **Set up a virtual environment** (optional but recommended)
```bash
python -m venv venv
```

3. **Activate the virtual environment**
```bash
source venv/bin/activate
```

4. **Install the project dependencies**
```bash
pip install -r requirements.txt
```

5. **Set up the .env file**
Copy the `.env.example` file to a new file named `.env`, and adjust the variables to fit your environment.

6. **Run the project**
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2
```