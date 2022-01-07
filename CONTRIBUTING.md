# Contribution Instruction & Guidelines

## Setup Repo

This repository uses [poetry](https://python-poetry.org/) for dependency management.
To setup all dependencies, install it and then run

```
poetry install
```

in this folder.

Poetry is also used for building and publishing the library.
This is normally handled by the corresponding [github action](.github/workflows/publish.yml),
but can also be done manually with

```
poetry publish --build
```

in this folder. The built package is hosted on [PyPI](https://pypi.org/project/confz/).

## Run Tests

[Pytest](https://pytest.org) is used for testing the code, together with [coverage](https://coverage.readthedocs.io).
To run all tests and build a coverage report, run

```
pytest --cov=confz
```

in this folder. To get an in-depth analysis of the coverage, generate a report, e.g. in HTML format, with

```
coverage html
```

in this folder. This will read the _.coverage_ file and generate a report out of it.

## Build Docs

[Sphinx](https://sphinx-doc.org/) is used for documentation, together with reST docstrings.
A corresponding github webhook triggers builds on [readthedocs](https://readthedocs.org/).
The documentation can also be built locally with 

```
make html
```

in the [docs](docs) folder.

## Branching & Release Strategy

The default branch is called _main_.
It contains the latest features, which would be ready for deployment.
It is not possible to push to it directly.
Instead, for every feature, a branch should be created, which will then be merged back into _main_ with a pull request.
Github is configured to run all tests when a PR is created.

At some point, a new version can be released.
To do so, a separate PR should be opened, which increases the version number.
After merging, a release with corresponding release notes can then be generated on Github.
This also automatically triggers a deployment to PyPI.

Semantic versioning is used for releases.
Branches should be prefixed with _feature/_, _bugfix/_ or _release/_ accordingly. 
