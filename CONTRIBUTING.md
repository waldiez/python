# How to contribute to this project

## Getting Started

This project is a Python package managed with [uv](https://github.com/astral-sh/uv) and [hatch](https://github.com/pypa/hatch). To get started, clone the repository and install the dependencies:

```bash
git clone ssh://github.com/waldiez/python.git -b dev
cd waldiez
# install uv if not already installed
python -m pip install uv
# generate a new venv
uv venv --python 3.10  # 3.10, 3.11, 3.12
# upgrade pip
uv pip install --upgrade pip
# activate the venv
. .venv/bin/activate
# on windows
# .venv\Scripts\activate.ps1 or .venv\Scripts\activate.bat
# install the dependencies
pip install -r requirements/all.txt
```

When ready, you can create a new branch and start working on your changes:

```bash
git checkout -b feature/my-feature
```

Once you are done, you can run the tests and check the code style:

```bash
make format
make lint
make test
```

If everything is fine, you can commit your changes and push them to the repository:

```bash
git add .
git commit -m "feat: my feature"
git push origin feature/my-feature
```

Finally, you can open a pull request on GitHub (use the dev branch as the target branch).

## Development

There are two core modules in this project:

- `waldiez.models`: Contains the pydantic models for the waldiez flow.
- `waldiez.exporting`: Contains the logic to export a waldiez flow to a python script or a jupyter notebook.

The project is structured as follows:

``` bash
waldiez
├── __main__.py
├── cli.py
├── cli_extras.py
├── exporter.py
├── runner.py
├── exporting
│   ├── agents
│   │   ...
│   ├── chats
│   │   ...
│   ├── flow
│   │   ...
│   ├── models
│   │   ...
│   ├── skills
│   │   ...
│   └── utils
│       ...
├── models
│   ├── agents
│   │   ...
│   ├── chat
│   │   ...
│   ├── common
│   │   ...
│   ├── flow
│   │   ...
│   ├── model
│   │   ...
│   └── skill
│       ...
├── _version.py
```

## Testing

To run the tests, you can use the following commands:

```bash
# for all tests
make test
# for specific tests
make test_models
make test_exporting
```
