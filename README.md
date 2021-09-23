# python-metadata

Python package to fetch the metadata of Python packages.

Uses PEP 621 metadata, if available otherwise PEP 517's
`prepare_metadata_for_build_wheel`, and lastly PEP 517's `build_wheel`.
