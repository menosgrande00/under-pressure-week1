
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class CameraMonitor(Node):

    def __init__(self):
        super().__init__('camera_monitor')

        # Alınan toplam kamera mesajı sayısı
        self.image_count = 0
        self.previous_count = 0

        # Henüz görüntü almadığımız için başlangıç değerleri
        self.width = 0
        self.height = 0
        self.encoding = 'unknown'

        # Gazebo'dan ROS'a aktarılan kamera topic'ine abone ol.
        # Sensor data QoS, görüntü gibi sensör verilerine uygundur.
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            qos_profile_sensor_data
        )

        # Her saniye kamera durumunu raporla.
        self.timer = self.create_timer(1.0, self.report_status)

    def image_callback(self, msg):
        # Her yeni görüntü mesajında bu fonksiyon çağrılır.
        self.image_count += 1

        # Görüntünün metadata bilgilerini kaydediyoruz.
        self.width = msg.width
        self.height = msg.height
        self.encoding = msg.encoding

    def report_status(self):
        # Son rapordan beri kaç yeni görüntü geldi?
        new_images = self.image_count - self.previous_count

        self.get_logger().info(
            f'Width: {self.width} | '
            f'Height: {self.height} | '
            f'Encoding: {self.encoding} | '
            f'Total: {self.image_count} | '
            f'New: {new_images}'
        )

        # Bir sonraki rapor için sayacı hatırla.
        self.previous_count = self.image_count


def main(args=None):
    rclpy.init(args=args)
    node = CameraMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
