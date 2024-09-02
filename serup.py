from setuptools import setup, Extension

module = Extension("factorizer", sources=["factorizer.c"])

setup(
    name="factorizer",
    version="1.0",
    description="A Python module for prime factorization",
    ext_modules=[module],
)
