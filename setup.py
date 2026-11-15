import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'up_week1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),

        ('share/' + package_name, ['package.xml']),

        # Launch dosyalarını kurulum klasörüne ekle.
        (os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.py')),

        # Gazebo dünyasını kurulum klasörüne ekle.
        (os.path.join('share', package_name, 'worlds'),
        glob('worlds/*.sdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='camm5',
    maintainer_email='camm5@todo.todo',
    description='Under Pressure AUV Week 1 ROS 2 simulation',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },

    entry_points={
        'console_scripts': [
            'heartbeat_publisher = up_week1.heartbeat_publisher:main',
            'heartbeat_subscriber = up_week1.heartbeat_subscriber:main',
            'camera_monitor = up_week1.camera_monitor:main',
        ],
    },

)
