# Introduction

Hi, My name is Geoffrey Knox, and this was my submission for the TMC (The Miles Consultancy) technical test.

In the root level of this project are a few different folders - most importantly the `api` and `frontend` folders. The `api` folder contains the FastAPI portion of the test, written using the [uv](https://docs.astral.sh/uv/) project manager. The `frontend` folder contains a [NextJS](https://nextjs.org/) application that can interact with the API. Also in the root level of the project are docker files for creating the images and building/starting containers with compose. The Dockerfiles for each application exist in their own respective folders.

## Note
I'm genuinely frustrated with how this process turned out. It wasted hours of my time and never even yielded a single interview to discuss the reasoning behind my approach. The only feedback I received was that "one or two things stood out" with no explanation beyond that. This is not a good way to treat candidates and it offers zero opportunity for growth on either side. Frankly, I have to ask: does TMC even know what they want? I solved the (flawed) tech test essentially perfectly, but somehow that wasn't enough. The double standard is intensely palpable: *"our process can be flawed, but you must be absolutely perfect and more!"*. Apparently the real puzzle wasn't the technical test, it was guessing what TMC actually wanted.

# Requirements
- Docker

**Dev Requirements**
- [uv](https://docs.astral.sh/uv/) (for debugging API, you might have some trouble using the CLI tool in the vscode terminal as uv is installed in the user path by default, and vscode seems to use the system path)
- [NodeJS>=20](https://nodejs.org/) (for frontend)
- [vscode](https://code.visualstudio.com/) (easiest for working with provided launch.json debugger configurations)

# Quick Start

In compliance with the test requirements, you can start all three services (postgresql, api, and frontend) using the following command in your CLI of choice:
```
docker compose up -d
```
For further testing/debugging, I've included some extra detail below.

# API

The API is written using the FastAPI framework, and uses dependency injection on each router endpoint to manage database access through the accompanying service for that endpoint (or other services if needed).

## VSCode Debugging

This project uses `uv` for project management, and is required for running and debugging. To start a debugging session, follow the instructions below to set it up:

Ensure that postgres is started before trying to debug this, as no connection to postgres will cause the program to crash. The easiest way to do this is by typing `docker compose up -d postgres` in the project root.

```bash
cd api # change to api directory
uv venv # create a venv for the api
uv sync # sync project requirements to virtual environment
```

**Important** Change vscode's default python interpreter to use the newly created venv by typing `Ctrl+Shift+P` to open the command palette, type `Python: Select Interpreter`, and find your newly created venv and select it.

Now, to start debugging, hit `Ctrl+Shift+D` to enter the vscode `Run and Debug` context, set the configuration to `API Debug` and hit the "play" button, or press F5 (by default).

## Start using `uv`

You can start the API without a debugging session by either typing `docker compose up -d fast_api` or you can use the terminal:

```bash
cd api # change to api directory
uv venv # create a venv for the api
uv sync # sync project requirements to virtual environment
```

Then to start the program (non-debuggable): `uv run test_api`

# Frontend

This project uses NextJS as a frontend react framework, so NodeJS is required to run and debug.

## VSCode Debugging

The easiest way to do this is to run two different debug configurations that are included. Hit `Ctrl+Shift+D` to enter vscode's `Run and Debug` window, then start the first configuration `Next.js: debug server-side`. Once that has started, open a browser debug session by starting the second configuration `Next.js: debug client-side`. See `.vscode/launch.json` for setting specific environment variables.

## Start using CLI

You can start the frontend without using a vscode debugging configuration by typing the following into the vscode terminal:

```bash
cd frontend # change to frontend directory
npm i # install project requirements
npm run dev # start the project in dev mode
```
