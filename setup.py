import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("limitedinteraction/VERSION", "r") as fh:
    version = fh.read()

setuptools.setup(
    name='limitedinteraction',
    version=version,
    description='Provides simple, backend-independant GUI tools for limited user interaction.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/felixchenier/limitedinteraction',
    author='Félix Chénier',
    author_email='chenier.felix@uqam.ca',
    license='Apache',
	license_files=['LICENSE'],
    packages=setuptools.find_packages(),
    package_data={
        'limitedinteraction': ['VERSION', 'images/*.png']},
    project_urls={
        'Source': 'https://github.com/felixchenier/limitedinteraction/',
        'Tracker': 'https://github.com/felixchenier/limitedinteraction/issues',
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: User Interfaces',
    ],
    python_requires='>=3.7',
)
