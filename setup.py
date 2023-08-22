from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pap",
    version="0.0.1",
    author="MOBR Systems",
    author_email="contact@mobr.ai",
    description="a Polkadot Analytics Platform",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mobr-ai/PolkadotAnalytics",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
