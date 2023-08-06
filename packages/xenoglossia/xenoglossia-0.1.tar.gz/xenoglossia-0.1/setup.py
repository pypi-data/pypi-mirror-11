from setuptools import setup

setup(
    name="xenoglossia",
    description="Robust(?) string manipulation language",
    author="Misty De Meo",
    author_email="mistydemeo@gmail.com",
    license="kindest",
    version="0.1",
    packages=["xenoglossia"],
    entry_points={"console_scripts": ["xg = xenoglossia.main:main"]},
)
