from setuptools import setup, find_packages

setup(
    name="youtube-uploader",
    version="1.0.0",
    author="Anushka",
    author_email="",
    description="🌸 A  YouTube video uploader built with Tkinter",
    packages=find_packages(),
    install_requires=[
        "google-auth-oauthlib",
        "google-api-python-client",
        "tk",
    ],
    entry_points={
        "console_scripts": [
            "video-upload = youtube_uploader.youtube_gui_uploader:main",
        ],
    },
    include_package_data=True,
    python_requires=">=3.8",
)
