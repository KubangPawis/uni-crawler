from setuptools import find_packages, setup

setup(
    name="uni_crawler",
    packages=find_packages(exclude=["uni_crawler_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
