# Process to Release a new PolyQEnt Version
This document is intended as a knowledge base for future additions requiring a new build and release of the whole project. When following these steps, in the end, the new version is published to the python package index (PyPI) and a new release is added to the GitHub repository containing binaries.

## Step 1: Make changes
Add new features and bug fixes via commits or pull requests to the main branch.

## Step 2: Update version number
Update the version number in `pyproject.toml` to reflect the new version. This is important for PyPi to recognize the new version and for pip to allow for package updates.

## Step 3: Create new version tag
Use the git command line tool to create a new tag of the format 'v[0-9]+.[0-9]+.[0-9]+':
```bash
git tag v*.*.*
```

## Step 4: Push the tag
In order to initiate the build and release process via the GitHub workflow, now push the tag:
```bash
git push origin v*.*.*
```
## Step 5: Verify
Lastly check on GitHub under the repository `Actions`, that everything worked (all green checkmarks). This can take a few minutes. 
