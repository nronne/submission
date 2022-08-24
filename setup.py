from setuptools import setup, find_packages

setup(
    name="submission",
    version="0.0.0",
    description="",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'array=submit:array',
            'sub=submit:sub'
        ]
    },
    python_requires=">=3.5",
)
