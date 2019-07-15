import setuptools

setuptools.setup(
    name="sys_moni",
    version="0.1.0",
    author="Margarita Markova",
    author_email="margarita_markova@epam.com",
    description="Monitor your system",
    scripts=['sys_moni.py'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
)
