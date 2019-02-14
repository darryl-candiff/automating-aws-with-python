from setuptools import setup

setup(
    name='webotron-80',
    version='0.1',
    author="Darryl Candiff",
    author_email='darryl@ccservices.nl',
    description="Webotron 80 is a demo tool to deploy static websites to AWS",
    license="GPLv3+",
    packages=['webotron'],
    url="https://github.com/darryl-candiff/automating-aws-with-python",
    install_requires=[
    'click',
    'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    ''',

)
