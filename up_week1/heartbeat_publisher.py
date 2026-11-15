
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


# Node sınıfından kalıtım alarak kendi ROS düğümümüzü oluşturuyoruz.
class HeartbeatPublisher(Node):

    # __init__ nesne oluşturulduğunda otomatik çalışır (constructor).
    def __init__(self):
        # Üst sınıfın constructor'ını çağırıp düğüme isim veriyoruz.
        super().__init__('heartbeat_publisher')

        # String tipindeki mesajları /up/heartbeat topic'ine yayınlar.
        # 10, QoS geçmiş derinliğidir (mesaj kuyruğuyla ilgilidir).
        self.publisher = self.create_publisher(
            String, '/up/heartbeat', 10
        )

        self.counter = 0  # Gönderilen mesajların sıra numarası

        # Her 1 saniyede bir send_message fonksiyonunu çağırır.
        self.timer = self.create_timer(1.0, self.send_message)

    def send_message(self):
        self.counter += 1

        # ROS String mesaj nesnesi oluşturuyoruz.
        msg = String()
        msg.data = f'Omer Faruk Onal - {self.counter}'

        # Mesajı topic üzerinden yayınlıyoruz.
        self.publisher.publish(msg)

        # Gönderilen mesajı terminalde gösteriyoruz.
        self.get_logger().info(msg.data)


def main(args=None):
    rclpy.init(args=args)  # ROS 2 Python sistemini başlatır.

    node = HeartbeatPublisher()  # Düğüm nesnesini oluşturur.

    try:
        # ROS olaylarını ve timer callback'lerini işler.
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass  # Ctrl+C ile durdurulması normaldir.
    finally:
        node.destroy_node()  # Düğüm kaynaklarını temizler.
        if rclpy.ok():
            rclpy.shutdown()  # ROS sistemini kapatır.


if __name__ == '__main__':
    main()
