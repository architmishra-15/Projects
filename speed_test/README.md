# About

The project is a simple web based speed testing program written in `Python` with fron UI in `Vite + React` in `JavaScript`.

## Setup

### Installation

To run this project locally, follow these steps -

- Install `node` and `npm` if haven't already. And run this command -
    ```bash
    npm create vite@latest speed-test -- --template react
    cd speed test
    ```
- Clone the repo using this command -
    ```bash
    git clone --filter=blob:none --no-checkout https://github.com/architmishra-15/Projects.git
    cd Projects
    git sparse-checkout init --speed_test
    git sparse-checkout set docs
    git pull origin main
    ```
    You can either in the newly created `speed-test` directory or somewhere else and replace the existing `App.jsx` and `package.json` with the files provided. After all that, run this command -
    ```bash
    npm install
    ```
- Install `tailwindcss` by following the process given on the [official website](https://tailwindcss.com/docs/guides/vite).

### Running -

- Run the command to start the server
    ```bash
    npm run dev
    ```
- Run the python code
     ```bash
     uvicorn main:app --reload
     ```
#### Open the browser and type `localhost:5173`.
