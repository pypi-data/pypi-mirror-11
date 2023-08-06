import sys

from distutils.command.build import build
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = "0.2.post7"

# Ubuntu 14.04 version.  Note: it's important that we build against the
# lowest version that we want to support or the pre-generated source that we
# ship in the tar.gz will not compile.
CFFI_MIN_VERSION = "0.8.2"

SETUP_REQUIRES_ERROR = (
    "Requested setup command that needs 'setup_requires' while command line "
    "arguments implied a side effect free command or option."
)

NO_SETUP_REQUIRES_ARGUMENTS = [
    "-h", "--help",
    "-n", "--dry-run",
    "-q", "--quiet",
    "-v", "--verbose",
    "-v", "--version",
    "--author",
    "--author-email",
    "--classifiers",
    "--contact",
    "--contact-email",
    "--description",
    "--egg-base",
    "--fullname",
    "--help-commands",
    "--keywords",
    "--licence",
    "--license",
    "--long-description",
    "--maintainer",
    "--maintainer-email",
    "--name",
    "--no-user-cfg",
    "--obsoletes",
    "--platforms",
    "--provides",
    "--requires",
    "--url",
    "clean",
    "egg_info",
    "register",
    "sdist",
    "upload",
]


def get_ext_modules():
    import posix_spawn._lib
    return [posix_spawn._lib.ffi.verifier.get_extension()]


class CFFIBuild(build):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        build.finalize_options(self)


class CFFIInstall(install):
    def finalize_options(self):
        self.distribution.ext_modules = get_ext_modules()
        install.finalize_options(self)


class DummyCFFIBuild(build):
    def run(self):
        raise RuntimeError(SETUP_REQUIRES_ERROR)


class DummyCFFIInstall(install):
    def run(self):
        raise RuntimeError(SETUP_REQUIRES_ERROR)


def keywords_with_side_effects(argv):
    def is_short_option(argument):
        """Check whether a command line argument is a short option."""
        return len(argument) >= 2 and argument[0] == '-' and argument[1] != '-'

    def expand_short_options(argument):
        """Expand combined short options into canonical short options."""
        return ('-' + char for char in argument[1:])

    def argument_without_setup_requirements(argv, i):
        """Check whether a command line argument needs setup requirements."""
        if argv[i] in NO_SETUP_REQUIRES_ARGUMENTS:
            # Simple case: An argument which is either an option or a command
            # which doesn't need setup requirements.
            return True
        elif (is_short_option(argv[i]) and
              all(option in NO_SETUP_REQUIRES_ARGUMENTS
                  for option in expand_short_options(argv[i]))):
            # Not so simple case: Combined short options none of which need
            # setup requirements.
            return True
        elif argv[i - 1:i] == ['--egg-base']:
            # Tricky case: --egg-info takes an argument which should not make
            # us use setup_requires (defeating the purpose of this code).
            return True
        else:
            return False

    if all(argument_without_setup_requirements(argv, i)
           for i in range(1, len(argv))):
        return {
            "cmdclass": {
                "build": DummyCFFIBuild,
                "install": DummyCFFIInstall,
            }
        }
    else:
        return {
            "setup_requires": [
                "cffi>=%s" % CFFI_MIN_VERSION,
            ],
            "cmdclass": {
                "build": CFFIBuild,
                "install": CFFIInstall,
            }
        }


setup(
    name="posix-spawn",
    version=VERSION,
    description="CFFI bindings to posix_spawn.",
    license="MIT",
    packages=find_packages(),
    package_data={
        "posix_spawn": ["c/*.c", "c/*.h"],
    },
    install_requires=[
        "cffi>=%s" % CFFI_MIN_VERSION,
    ],
    zip_safe=False,
    **keywords_with_side_effects(sys.argv)
)
