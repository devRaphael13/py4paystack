from setuptools import setup, find_packages


setup(

    # Project name:

    name='py4paystack',

    # Packages to include in the distribution:

    packages=find_packages(),

    # Project version number:

    version='1.0.2',

    # List a license for the project, eg. MIT License

    license='MIT License',

    # Short description of your library:

    description='A paystack API wrapper in python with optional type checking functionality',

    # Long description of your library:

    long_description_content_type='text/markdown',

    # Your name:

    author='Raphael Ezeigwe',

    # Your email address:

    author_email='iraphael1308@gmail.com',

    # Link to your github repository or website:

    url='https://github.com/devRaphael13/py4paystack/issues',

    # Download Link from where the project can be downloaded from:

    download_url='https://github.com/devRaphael13/py4paystack',

    # List of keywords:

    keywords=["python", "paystack"],

    # List project dependencies:

    install_requires=["python-dotenv"],

    # https://pypi.org/classifiers/

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    
    python_requires='>=3.9',

)