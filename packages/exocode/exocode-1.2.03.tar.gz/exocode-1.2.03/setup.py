from setuptools import setup

setup(name='exocode',
    version='1.2.03',
    description='Automation of debris disk detection',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Astronomy'
    ],
    keywords = 'exoplanets astronomy astrophysics circumstellar disks',
    url='https://bitbucket.org/leckman/exoplanets',
    author='Laura Eckman',
    author_email='leckman@mit.edu',
    license='MIT',
    packages=['src'],
    install_requires=[
        'matplotlib',
        'scikit-image',
        'numpy',
        'astropy',
    ],
    include_package_data=True,
    zip_safe=False)
