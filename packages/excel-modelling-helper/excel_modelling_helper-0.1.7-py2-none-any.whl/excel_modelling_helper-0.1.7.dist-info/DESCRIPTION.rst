# Doc
[https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html#uploading-your-project-to-pypi]

# Build

`python setup.py sdist`

# Upload
It might be necessary to first delete old packages in 'dist' folder
`twine upload dist/*`

# Local install

## Build wheel
`python setup.py bdist_wheel -d dist`

15.5.2015   0.1.1   Renamed class to ParameterLoader
22.5.2015   0.1.2   Add sheet index as parameter to loader

