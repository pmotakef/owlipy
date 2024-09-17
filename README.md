# OWLIPy
Optimization Wrapper for Linear/Integer Programming


# Bumpver
To update the version use `bumpver` as following

```commandline
bumpver update --[patch|minor|major]
```
This will update the version, commits the changes and tags the repo. But doesn't push.
Next use 
```commandline
git push origin --tags
```
To push the new tag

# Publish / Update in PyPI
Make sure `build` and `twine` are already installed.
```commandline
pip install build twine
```
To build the package navigate to the project directory and build the package using:
```commandline
python -m build
```
Check the distribution files to be ok using:
```commandline
twine check dist/*
```
At the end publish the package to PyPI using the following:
```commandline
twine upload dist/*
```
