from setuptools import find_packages, setup

package_name = 'lidar_app'

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
    maintainer='ir-t11',
    maintainer_email='martiaguilar04@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "lidar_publisher = lidar_app.lidar_publisher:main", "decision_subscriber = lidar_app.decision_subscriber:main",
        ],
    },
)
