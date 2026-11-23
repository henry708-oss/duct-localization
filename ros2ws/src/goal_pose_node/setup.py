from setuptools import find_packages, setup

package_name = 'goal_pose_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='henry708',
    maintainer_email='henry708@umn.edu',
    description='Publishes goal pose data to a robot given messages from the robot on its status',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'talker = goal_pose_node.publisher_member_function:main',
            'listener = goal_pose_node.subscriber_member_function:main',
        ],
    },
)
