from setuptools import setup

setup(
    name="artemis_service_websockets",
    version="0.1",
    packages=[
        "artemis_service_websockets"
    ],
    install_requires=[
        "gevent",
        "gevent-websocket",
        "haigha",
        "baseplate",
        "manhole",
    ],
)
