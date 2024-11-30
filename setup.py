from setuptools import setup, find_packages

setup(
    name='gemini-cellpose-agent',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'google-generativeai',
    ],
    entry_points={
        'console_scripts': [
            'run_demo=gemini_cell_agent.run_demo:main',
        ],
    },
    author='Xueer Chen',
    author_email='xueer.chen.human@gmail.com',
    description='An agent to automate cell research using Gemini',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/xueerchen1990/gemini-cell-agent',
    license='MIT',
)
