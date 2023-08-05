import os
import sys
import pytest
from pipsi import Repo, find_scripts


@pytest.fixture(params=['normal', 'MixedCase'])
def mix(request):
    return request.param


@pytest.fixture
def bin(tmpdir, mix):
    return tmpdir.ensure(mix, 'bin', dir=1)


@pytest.fixture
def home(tmpdir, mix):
    return tmpdir.ensure(mix, 'venvs', dir=1)


@pytest.fixture
def repo(home, bin):
    return Repo(str(home), str(bin))


@pytest.mark.parametrize('package, glob', [
    ('grin', 'grin*'),
    ('pipsi', 'pipsi*'),
])
def test_simple_install(repo, home, bin, package, glob):
    assert not home.listdir()
    assert not bin.listdir()
    repo.install(package)
    assert home.join(package).check()
    assert bin.listdir(glob)


@pytest.mark.xfail(sys.version_info[0] != 3,
                   reason='attic is python3 only')
def test_simple_install_attic(repo, home, bin):
    test_simple_install(repo, home, bin, 'attic', 'attic*')


def test_find_scripts():
    print('executable ' + sys.executable)
    env = os.path.dirname(
        os.path.dirname(sys.executable))
    print('env %r' % env)
    print('listdir %r' % os.listdir(env))
    scripts = list(find_scripts(env, 'pipsi'))
    print('scripts %r' % scripts)
    assert scripts
