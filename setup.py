from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=0.24.2", "requests>=2.22.0", "tqdm>=4.35.0", "osmapi>=1.2.2"]

setup(
    name="OSMEvolution",
    version="1.0",
    author="Leonard Vorbeck",
    author_email="leomxyy@googlemail.com",
    description="A package for receiving and restructuring OSM historic data conveniently",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/le0x99/OSMEvolution/",
    packages=find_packages(),
    install_requires=requirements,
        classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
