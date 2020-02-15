from setuptools import setup, find_packages

setup(
    name="JsonDataManager",
    license="MIT",
    version="1.0",
    author="PieSignal",
    author_email="leeon@insiro.me",
    url="https://github.com/PieSignal/JsonDataManager",
    requires=["typing >= 3.7.4.1, <4"],
    packages=find_packages(),
)
