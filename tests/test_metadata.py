# SPDX-License-Identifier: EUPL-1.2

import os
import pathlib

import metadata


package_dir = pathlib.Path(__file__).parent / 'packages'


def test_pep621():
    m = metadata.Metadata(package_dir / 'full-pep621')
    assert m.name == 'full-pep621'
    assert m.version == '3.2.1'
    assert m.requires_python == '>=3.8'
    assert m.license == 'some license text'
    assert m.readme == 'some readme\n'
    assert m.description == 'A package with all the metadata :)'
    assert m.authors == [
        ('Unknown', 'example@example.com'),
        ('Example!', None),
    ]
    assert m.maintainers == [
        ('Other Example', 'other@example.com'),
    ]
    assert m.keywords == ['trampolim', 'is', 'interesting']
    assert m.classifiers == [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
    ]
    assert m.urls == {
        'changelog': 'github.com/some/repo/blob/master/CHANGELOG.rst',
        'documentation': 'readthedocs.org',
        'homepage': 'example.com',
        'repository': 'github.com/some/repo',
    }
    # TODO: entrypoints
    # assert m.dependencies == [
    #     'dependency1',
    #     'dependency2>1.0.0',
    #     'dependency3[extra]',
    #     'dependency4; os_name != "nt"',
    #     'dependency5[other-extra]>1.0; os_name == "nt"',
    # ]
    # assert m.optional_dependencies == {
    #     'test': [
    #         'test_dependency',
    #         'test_dependency[test_extra]',
    #         'test_dependency[test_extra2]>3.0; os_name == "nt"',
    #     ],
    # }


def test_pep517():
    m = metadata.Metadata(package_dir / 'full-setup-cfg')
    assert m.name == 'full-setup-cfg'
    assert m.version == '3.2.1'
    assert m.requires_python == '>=3.8'
    assert m.license == 'some license text'
    assert m.readme == 'some readme\n\n\n'
    assert m.description == 'A package with all the metadata :)'
    assert m.authors == [
        ('Filipe Laíns', None),
        ('Unknown', 'lains@riseup.net'),
    ]
    assert m.maintainers == [
        ('Filipe Laíns', None),
        ('Unknown', 'lains@riseup.net'),
    ]
    assert m.keywords == ['trampolim', 'is', 'interesting']
    assert m.classifiers == [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
    ]
    assert m.urls == {
        'changelog': 'github.com/some/repo/blob/master/CHANGELOG.rst',
        'documentation': 'readthedocs.org',
        'homepage': 'example.com',
        'repository': 'github.com/some/repo',
    }
    # TODO: entrypoints
    # assert m.dependencies == [
    #     'dependency1',
    #     'dependency2>1.0.0',
    #     'dependency3[extra]',
    #     'dependency4; os_name != "nt"',
    #     'dependency5[other-extra]>1.0; os_name == "nt"',
    # ]
    # assert m.optional_dependencies == {
    #     'test': [
    #         'test_dependency',
    #         'test_dependency[test_extra]',
    #         'test_dependency[test_extra2]>3.0; os_name == "nt"',
    #     ],
    # }
