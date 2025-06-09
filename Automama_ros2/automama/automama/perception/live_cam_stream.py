import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=480,
    framerate=30,
    flip_method=0,
):
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width={capture_width}, height={capture_height}, framerate={framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width={display_width}, height={display_height}, format=BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=BGR ! appsink"
    )

class CameraHandler:
    def __init__(self, node, sensor_id, topic_name, window_name):
        self.node = node
        self.sensor_id = sensor_id
        self.topic_name = topic_name
        self.window_name = window_name
        self.publisher = node.create_publisher(Image, topic_name, 10)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(gstreamer_pipeline(sensor_id), cv2.CAP_GSTREAMER)

        if not self.cap.isOpened():
            node.get_logger().error(f"Failed to open CSI camera {sensor_id}")
            raise RuntimeError(f"Failed to open CSI camera {sensor_id}")

    def capture_and_publish(self):
        ret, frame = self.cap.read()
        if not ret:
            self.node.get_logger().error(f"Failed to capture frame from camera {self.sensor_id}")
            return

        # Publish ROS Image message
        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.publisher.publish(msg)

        # Visualize frame
        cv2.imshow(self.window_name, frame)


class CSIDualCameraPublisher(Node):
    def __init__(self):
        super().__init__('csi_dual_cam_publisher')

        # Create handlers for both cameras
        self.cam0 = CameraHandler(self, sensor_id=0, topic_name='/csi_cam_0', window_name='CSI Camera 0')
        self.cam1 = CameraHandler(self, sensor_id=1, topic_name='/csi_cam_1', window_name='CSI Camera 1')

        self.timer = self.create_timer(0.03, self.timer_callback)  # ~30 FPS

    def timer_callback(self):
        self.cam0.capture_and_publish()
        self.cam1.capture_and_publish()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.get_logger().info('Quit requested, shutting down...')
            rclpy.shutdown()

    def destroy_node(self):
        self.cam0.cap.release()
        self.cam1.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CSIDualCameraPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
