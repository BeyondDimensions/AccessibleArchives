from setuptools import setup, find_packages

setup(
    name='Lighthouse',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'transformers',
        'python-dotenv',
        'torch',
        'pymupdf',
        'opencv-python',
        'openai'
    ],
    extras_require={
        'all': ['pandoc', 'texlive', 'texlive-xetex', 'texlive-fonts-recommended']
    }
)
