from setuptools import setup, find_packages

setup(
    name="tr_address_locator",
    version="0.1",
    author="Elnaz Najatishendi",
    author_email="nejati.elnaz@gmail.com",
    description="Türkiye adreslerini koordinatlandırmak için Python kütüphanesi",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/kullanici_adi/tr_address_locator",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "geopy",
        "openpyxl"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
