from setuptools import setup, Extension

module = Extension("factorizer", sources=["factorizer.c"], libraries=["m"])

setup(
    name="factorizer",
    version="1.0",
    description="A Python module for factorizing numbers",
    ext_modules=[module],
)
