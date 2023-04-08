# RPS15 Online
This repository contains the frontend and backend source code for RPS15 Online.

## Outline
The project outline is available on [Google Drive](https://docs.google.com/document/d/1x0xAeOwBHWjecVnfBTDeRkyU-r3mhlzBU-41T72Rxng).

## Setup
This section describes how to set up the project for development. It will assume that you have cloned the repository using either `git clone https://github.com/mattrrubino/cse312-group-project.git` or `git clone git@github.com:mattrrubino/cse312-group-project.git`.

### Frontend
TODO

### API
To set up the API for development:

1. Install Python 3.11
2. `cd api`
3. `python -m venv venv`
4. Activate the virtual environment
    - Mac/Linux: `. venv/bin/activate`
    - Windows: `call venv/Scripts/activate` (may need to call cmd first if 'call' isn't working)
5. `pip install -r requirements.txt`
6. `python src/main.py`

You should now be able to view the API documentation at <http://localhost:8000/docs>.
Next time you want to develop, simply activate the virtual environment and run python.
