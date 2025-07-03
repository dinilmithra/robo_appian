from setuptools import setup, find_packages

setup(
    name='rombo_appian',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'selenium>=4.34.0'
          ],
    author='Dinil Mithra',
    author_email='dinilmithra@mailme@gmail.com',
    description='Automate your Appin code testing with Python. Boost quality, save time.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dinilmithra/robo_test_suite_appian.git', 
    classifiers=[
        'Programming Language :: Python :: 3',
        # 'License :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
