#!/bin/bash
## Increase the version of the project
## Optional parameter for version type. Accepted values are: major | minor | patch
VERSION_TYPE=${1:-patch}

if [[ "$VERSION_TYPE" != "patch" && "$VERSION_TYPE" != "minor" && "$VERSION_TYPE" != "major" ]]; then
    echo "Invalid version type: ${VERSION_TYPE}";
    exit 1;
fi

poetry version ${VERSION_TYPE}
version=`poetry version --short`
echo "Increased version to ${version}"
echo "Committing new version ${veresion}"
git add pyproject.toml
git commit -m "Version ${version}"
