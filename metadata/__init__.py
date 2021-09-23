# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import os
import pathlib
import sys

from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

import build.util
import pep621
import tomli


if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata

    from functools import cached_property
else:
    import importlib_metadata

    from backports.cached_property import cached_property


class Metadata:
    _FIELD_MAP: ClassVar[Dict[str, Optional[str]]] = {
        'name': 'Name',
        'version': 'Version',
        'description': 'Summary',
        'readme': 'Description',
        'license': 'License',
        'requires-python': 'Requires-Python',
        'authors': None,  # Author / Author-Email
        'maintainers': None,  # Maintainer / Maintainer-Email
        'keywords': 'Keywords',
        'classifiers': 'Classifier',
        'urls': None,  # Project URL
        # 'entrypoints': None,  # scripts, gui-scripts, entrypoints
        # 'dependencies': None,  # Requires-Dist / Provides-Extra
        # 'optional-dependencies': None,  # Requires-Dist / Provides-Extra
    }
    _FIELDS: ClassVar[List[str]] = list(_FIELD_MAP.keys()) + [
    ]

    def __init__(self, project_path: Union[str, os.PathLike[str]]) -> None:
        self._path = pathlib.Path(project_path)

        pyproject = self._path.joinpath('pyproject.toml')
        if pyproject.is_file():
            self._pyproject = tomli.loads(pyproject.read_text())
            self._has_pep621 = 'project' in self._pyproject
        else:
            self._has_pep621 = False

    def __dir__(self) -> List[str]:
        return list(super().__dir__()) + self._FIELDS

    def __getattr__(self, name: str) -> Any:
        name = name.replace('_', '-')
        if self._has_pep621 and name not in self._pep621_metadata.dynamic:
            return self._get_pep621_field(name)
        return self._get_core_metadata_field(name)

    @cached_property
    def _pep621_metadata(self) -> pep621.StandardMetadata:
        return pep621.StandardMetadata.from_pyproject(self._pyproject, self._path)

    @cached_property
    def _core_metadata(self) -> importlib_metadata.PackageMetadata:
        return build.util.project_wheel_metadata(self._path)

    def _get_pep621_field(self, name: str) -> Any:
        if name == 'version':
            return str(self._pep621_metadata.version)
        elif name == 'requires-python':
            return str(self._pep621_metadata.requires_python)
        elif name == 'readme':
            return self._pep621_metadata.readme.text
        elif name == 'license':
            return self._pep621_metadata.license.text
        # elif name == 'entrypoints':
        #     ...
        # elif name == 'dependencies':
        #     return list(map(str, self._pep621_metadata.dependencies))
        # elif name == 'optional-dependencies':
        #     return {
        #         entry: list(map(str, dependencies))
        #         for entry, dependencies in self._pep621_metadata.optional_dependencies.items()
        #     }
        elif name in self._FIELD_MAP:
            return getattr(self._pep621_metadata, name.replace('-', '_'))
        raise AttributeError(f'Project does not have `{name}` metadata field (PEP 621)')

    def _get_people_core_metadata(self, name: str) -> List[Tuple[str, Optional[str]]]:
        fields: List[Tuple[str, Optional[str]]] = []
        for entry in self._core_metadata.get_all(name):
            fields.append((entry, None))
        for entry in self._core_metadata.get_all(f'{name}-Email'):
            fields.append(('Unknown', entry))
        return fields

    def _get_core_metadata_field(self, name: str) -> Any:
        if name == 'authors':
            return self._get_people_core_metadata('Author')
        elif name == 'maintainers':
            return self._get_people_core_metadata('Maintainer')
        elif name == 'readme':
            return self._core_metadata.get_payload()
        elif name == 'keywords':
            return self._core_metadata.get('keywords', '').split(',')
        elif name == 'urls':
            urls = {}
            for value in self._core_metadata.get_all('Project-URL'):
                name, url = value.split(', ')
                urls[name] = url
            return urls
        # elif name == 'entrypoints':
        #     ...
        # elif name == 'dependencies':
        #     ...
        # elif name == 'optional-dependencies':
        #     ...
        elif self._FIELD_MAP.get(name):
            values = self._core_metadata.get_all(self._FIELD_MAP[name])
            if len(values) == 1:
                return values[0]
            return values
        raise AttributeError(f'Project does not have `{name}` metadata field (core metadata - PEP 517)')
