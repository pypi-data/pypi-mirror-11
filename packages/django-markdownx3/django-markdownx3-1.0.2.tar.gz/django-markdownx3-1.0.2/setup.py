from setuptools import setup, find_packages

import os
if 'vagrant' in str(os.environ):
    del os.link

setup(
    name='django-markdownx3',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    description='Simple markdown editor (without any UI controls) with image uploads (stored in MEDIA_ROOT folder) and live preview',
    url='https://github.com/pydanny/django-markdownx',
    author='adi-',
    author_email='aaadeji@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: JavaScript',
    ],
    keywords='django markdown live preview images upload',
    install_requires=['Pillow', 'Markdown'],
)
