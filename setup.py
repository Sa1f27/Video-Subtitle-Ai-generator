from setuptools import setup, find_packages

setup(
    name='Vid-Sub',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A web application to automatically generate and embed subtitles into videos.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your-username/Vid-Sub',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'email-validator>=2.2.0',
        'ffmpeg-python>=0.2.0',
        'flask>=3.1.2',
        'flask-sqlalchemy>=3.1.1',
        'gunicorn>=23.0.0',
        'moviepy>=2.2.1',
        'openai>=1.100.2',
        'psycopg2-binary>=2.9.10',
        'pydub>=0.25.1',
        'python-dotenv>=1.1.1',
        'requests>=2.31.0',
        'speechrecognition>=3.14.3',
        'srt>=3.5.3',
        'werkzeug>=3.1.3',
        'yt-dlp>=2025.8.20',
    ],
    entry_points={
        'console_scripts': [
            'vidsub=app:app',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
