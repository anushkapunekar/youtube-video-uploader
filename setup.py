from setuptools import setup, find_packages

setup(
    name="youtube-uploader",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "google-api-python-client",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "Pillow",
        "requests",
        "ffmpeg-python"
    ],
    entry_points={
        "console_scripts": [
            "video-upload = youtube_uploader.youtube_gui_uploader:main"
        ]
    },
)
