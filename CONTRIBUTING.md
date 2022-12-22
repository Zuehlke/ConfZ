# Contribution Instruction & Guidelines

Hello there! Any kind of contribution to ConfZ is most welcome!

- If you have a question, please use GitHub
  [discussions](https://github.com/Zuehlke/ConfZ/discussions).
- If you found a bug or have a feature request, please use GitHub
  [issues](https://github.com/Zuehlke/ConfZ/issues).
- If you fixed a bug or implemented a new feature, please do a pull request. If it
  is a larger change or addition, it would be great to first discuss thorugh an
  [issue](https://github.com/Zuehlke/ConfZ/issues).

## Setup Repo

This repository uses [poetry](https://python-poetry.org/) for dependency management.
To setup all dependencies, install it and then run

```
poetry install
```

in this folder.

Poetry is also used for building and publishing the library.
This is normally handled by the corresponding
[github action](github/workflows/publish.yml), but can also be done manually with

```
poetry publish --build
```

in this folder. The built package is hosted on [PyPI](https://pypi.org/project/confz/).

## Development Tools

[Pytest](https://pytest.org) is used for testing the code, just run

```
pytest -W error
```

in this folder. We strive for a coverage of 100%. To check this, run the following:

```
coverage run -m pytest
coverage report --fail-under=100
```

This repository furthermore uses [mypy](https://mypy.readthedocs.io/en/stable/) for 
type checking, which can be run with the following:

```
mypy confz
```

For linting, we use [pylint](https://pylint.org/), which can be run with:

```
pylint confz
```

Last but not least, we use [black](https://black.readthedocs.io/en/stable/) for 
formatting. You can reformat all files with:

```
black .
```

There are GitHub actions in place for all these tools which make sure that no pull 
request will be merged if any of them shows an error.

## Documentation

[Sphinx](https://sphinx-doc.org/) is used for documentation, together with reST 
docstrings. A corresponding github webhook triggers builds on
[readthedocs](https://readthedocs.org/). The documentation can also be built locally 
by running 

```
make html
```

in the [docs](docs) folder.

## Branching & Release Strategy

The default branch is called _main_. It contains the latest features, which would be 
ready for deployment. It is not possible to push to it directly. Instead, for every 
feature, a branch should be created, which will then be merged back into _main_ with 
a pull request. GitHub is configured to run all tests when a PR is created.

At some point, a new version can be released.
To do so, a release with corresponding release notes can then be generated on GitHub.
This also automatically triggers a deployment to PyPI. The tag of the release should 
match the version specified in [pyproject.toml](pyproject.toml).

Semantic versioning is used for releases.
