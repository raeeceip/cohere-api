from setuptools import setup, find_packages

setup(
    name="commandr",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0",
        "cohere>=4.0.0",
        "python-dotenv>=1.0.0",
        "markdown>=3.4.3",
        "pygments>=2.15.1",
        "pyinstaller>=5.13.0",
        "pillow>=10.0.0"
    ],
    entry_points={
        "console_scripts": [
            "commandr=src.main:main",
        ],
    },
    package_data={
        "": ["resources/*"],
    },
    python_requires=">=3.8",
)
