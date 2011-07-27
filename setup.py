from setuptools import setup, find_packages

setup(
    name='news',
    version='0.1',
    description='News application for ATVC',
    author='outsider',
    author_email='outsider@atvc.ru',
    url='http://www.atvc.ru',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
