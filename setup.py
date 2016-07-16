from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django_helpcenter',
    version='0.6.0',
    description='Django app for creating a help section',
    long_description=readme(),
    url='http://github.com/smalls12/django_helpcenter',
    author='Chathan Driehuys',
    author_email='cdriehuys@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['example_project']),
    include_package_data=True,
    install_requires=[
        'django',
        'djangorestframework',
        'pytz',
    ],
    zip_safe=False)
