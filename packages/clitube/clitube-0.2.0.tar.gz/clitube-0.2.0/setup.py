from setuptools import setup


VERSION = "0.2.0"
DESCRIPTION = "Browse and listen Youtube video soundtrack from your terminal"

setup(
    name="clitube",
    version=VERSION,
    author="NiZiL",

    url="https://github.com/NiZiL/clitube",
    download_url="https://github.com/NiZiL/clitube/tarball/"+VERSION,

    description=DESCRIPTION,
    keywords=['YouTube', 'CLI'],
    classifiers=[],

    packages=['clitube'],
    scripts=['scripts/clitube'],

    install_requires=['requests', 'youtube-dl']
)
