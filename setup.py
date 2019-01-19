import setuptools

setuptools.setup(
    name='rafl',
    version='0.1.0',
    description='RAFL Web Helpers',
    author='rplnt',
    python_requires='>=3.6.0',
    packages=setuptools.find_packages(exclude=('tests',)),

    entry_points={
        'console_scripts': ['rafl-scrape=scraper.pcs_rankings:main'],
    },
    install_requires=[
        'requests',
        'beautifulsoup4',
        'flake8',
    ]
)