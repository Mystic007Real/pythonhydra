from setuptools import setup, find_packages

setup(
    name="pythonhydra",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pycryptodome",
        "pyinstaller"
    ],
    entry_points={
        "console_scripts": [
            "pythonhydra=pythonhydra.obfuscate:main",
        ],
    },
    author="Your Name",
    description="A Python script obfuscator that converts Python scripts to encrypted EXE files.",
    url="https://github.com/Mystic007Real/pythonhydra",
)
