from setuptools import find_packages, setup

package_name = 'automama'

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
    maintainer='deen',
    maintainer_email='deen@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'talker = automama.test.talker:main',  # ✅ Note quotes are balanced!
        'segmentation = automama.perception.road_segment:main',
        'csi_cam_stream = automama.perception.live_cam_stream:main',
        'manual_control = automama.control.manual_control:main',
        ],
    },
)
