from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyzapzure",
    version="0.1.0",
    author="emanuel",
    author_email="roqueemanuel2018@gmail.com",
    description="Automatização de envio de mensagens para WhatsApp usando Python e Selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/pyzapzure",
    project_urls={
        "Bug Tracker": "https://github.com/emanuel-git-bot/pyzapzure/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "selenium>=4.10.0",
        "pillow>=9.5.0",
        "webdriver-manager>=3.8.5"
    ],
) 