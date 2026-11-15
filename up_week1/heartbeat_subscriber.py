
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HeartbeatSubscriber(Node):

    def __init__(self):
        # ROS düğümümüzün adı
        super().__init__('heartbeat_subscriber')

        # /up/heartbeat topic'ine abone oluyoruz.
        # Her yeni mesaj geldiğinde receive_message çağrılır.
        self.subscription = self.create_subscription(
            String,
            '/up/heartbeat',
            self.receive_message,
            10
        )

    # Gelen ROS mesajı callback'e parametre olarak aktarılır.
    def receive_message(self, msg):
        self.get_logger().info(f'Received: {msg.data}')


def main(args=None):
    rclpy.init(args=args)

    node = HeartbeatSubscriber()

    try:
        # Gelen mesajları işlemek için düğümü çalışır tutar.
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
