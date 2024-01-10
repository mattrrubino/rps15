# RPS15 Online
This repository contains the frontend and backend source code for RPS15 Online.

## Outline
The project outline is available on [Google Drive](https://docs.google.com/document/d/1x0xAeOwBHWjecVnfBTDeRkyU-r3mhlzBU-41T72Rxng).

## Quickstart
To try out the project, run `docker compose up` and open <http://localhost>. In order for a game to start, at least two users need to be queued. To simulate this, open two browsers, create different accounts in both browsers, and then click `Play` in both browsers.

### Frontend
To set up the frontend for development, install [Node with npm](https://nodejs.org/en/download). Then, do the following:

1. `cd frontend`
2. `npm i`
3. `npm run dev`

You should be able to view the frontend at <http://localhost:5173>.
Next time you want to develop, simply run `npm run dev` from the `frontend` directory.
Finally, to create a production build, execute `npm run build`. The build will be located in the `dist` directory.

### API
To set up the API for development, install [Python 3.11](https://www.python.org/downloads/release/python-3110/) and [MongoDB](https://www.mongodb.com/try/download/community). Then, do the following:

1. `cd api`
2. `python -m venv venv`
3. Activate the virtual environment
    - Mac/Linux: `. venv/bin/activate`
    - Windows: `call venv/Scripts/activate` (may need to call cmd first if 'call' isn't working)
4. `pip install -r requirements.txt`
5. `python src/main.py`

You should now be able to view the API documentation at <http://localhost:8000/docs>.
Next time you want to develop, simply run `dev` from the `api` directory.
