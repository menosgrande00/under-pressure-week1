
import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Paketin kurulduğu konumu ROS üzerinden buluyoruz.
    # Böylece bilgisayara özel sabit dosya yolu kullanmıyoruz.
    package_path = get_package_share_directory('up_week1')

    world_path = os.path.join(
        package_path, 'worlds', 'test_world.sdf'
    )

    # Gazebo simülasyonunu OGRE 1 ile başlatıyoruz.
    gazebo = ExecuteProcess(
        cmd=[
            'ign', 'gazebo', '-r',
            world_path,
            '--render-engine', 'ogre'
        ],
        output='screen'
    )

    # Gazebo kamera görüntüsünü ROS Image mesajına çevirir.
    camera_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/camera/image_raw@sensor_msgs/msg/Image[ignition.msgs.Image'
        ],
        output='screen'
    )

    # Kamera görüntüsünü takip eden kendi düğümümüz.
    camera_monitor = Node(
        package='up_week1',
        executable='camera_monitor',
        output='screen'
    )

    # Her saniye heartbeat mesajı yayınlar.
    heartbeat_publisher = Node(
        package='up_week1',
        executable='heartbeat_publisher',
        output='screen'
    )

    # Heartbeat mesajlarına abone olur.
    heartbeat_subscriber = Node(
        package='up_week1',
        executable='heartbeat_subscriber',
        output='screen'
    )

    # Bütün bileşenleri tek launch ile başlatır.
    return LaunchDescription([
        gazebo,
        camera_bridge,
        camera_monitor,
        heartbeat_publisher,
        heartbeat_subscriber
    ])
