from setuptools import setup, find_packages

from asciimap import meta


setup(
    name=meta.display_name,
    version=meta.version,
    description=meta.description,
    long_description=meta.long_description,
    author=meta.author,
    author_email=meta.author_email,
    url=meta.url,
    license=meta.license,
    packages=find_packages(),
    install_requires=meta.requires,
    zip_safe=False
    )
