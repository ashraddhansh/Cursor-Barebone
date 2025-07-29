# Cursor Barebone

- This is a small AI agent project that works rudimentary like LLM code agents(example: cursor, claude).
- It is powered by Gemini AI.

It uses 4 basic functions to solve the problem specified by the user:

- `get_file_content`: fetches the content of the file so the agent can read it.
- `get_files_info`: fetches the directory structure.
- `run_python`: run the python code so agent can test the implemented solutions.
- `write_file`: write the content provided by agent into a file.

## Project Structure

```
.
├── calculator
│   ├── gemini.py
│   ├── lorem.txt
│   ├── main.py
│   ├── pkg
│   │   ├── calculator.py
│   │   ├── morelorem.txt
│   │   ├── __pycache__
│   │   │   ├── calculator.cpython-313.pyc
│   │   │   └── render.cpython-313.pyc
│   │   └── render.py
│   ├── README.md
│   └── tests.py
├── call_function.py
├── config.py
├── functions
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── __pycache__
│   │   ├── constants.cpython-313.pyc
│   │   ├── get_file_content.cpython-313.pyc
│   │   ├── get_files_info.cpython-313.pyc
│   │   ├── run_python.cpython-313.pyc
│   │   └── write_file.cpython-313.pyc
│   ├── run_python.py
│   └── write_file.py
├── main.py
├── __pycache__
│   ├── call_function.cpython-313.pyc
│   └── config.cpython-313.pyc
├── pyproject.toml
├── README.md
├── tests.py
└── uv.lock

7 directories, 28 files
```
