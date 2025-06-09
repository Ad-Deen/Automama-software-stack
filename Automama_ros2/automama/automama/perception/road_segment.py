import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from ultralytics import YOLO


class RoadSegmentNode(Node):
    def __init__(self):
        super().__init__('road_segment_node')

        self.model = YOLO("/home/deen/ros2_ws/src/automama/automama/perception/yolov8s.engine", task="segment")
        self.target_class_name = "road"

        self.get_logger().info("YOLOv8 segmentation model loaded. Starting video stream...")

        self.run()

    def run(self):
        results = self.model.predict(source="/home/deen/ros2_ws/src/automama/automama/perception/killo_road.mp4", stream=True)

        for r in results:
            frame = r.orig_img.copy()

            if r.masks is not None and r.masks.data is not None and r.boxes.cls is not None:
                masks = r.masks.data.detach().cpu().numpy()
                classes = r.boxes.cls.detach().cpu().numpy().astype(int)
                class_names = self.model.names

                combined_mask = np.zeros(frame.shape[:2], dtype=np.uint8)

                for i, cls_idx in enumerate(classes):
                    if class_names[cls_idx] == self.target_class_name:
                        binary_mask = (masks[i] > 0.5).astype(np.uint8)

                        if binary_mask.shape != frame.shape[:2]:
                            binary_mask = cv2.resize(binary_mask, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

                        combined_mask = np.maximum(combined_mask, binary_mask)

                new_height = combined_mask.shape[0] * 2
                new_width = combined_mask.shape[1]
                combined_mask_resized = cv2.resize(combined_mask, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

                combined_mask_color = np.zeros((combined_mask_resized.shape[0], combined_mask_resized.shape[1], 3), dtype=np.uint8)
                combined_mask_color[:, :, 2] = combined_mask_resized * 255

                cv2.imshow("Original Frame", frame)
                cv2.imshow("Road Mask (Height x2)", combined_mask_color)
            else:
                blank_mask = np.zeros((frame.shape[0]*2, frame.shape[1], 3), dtype=np.uint8)
                cv2.imshow("Original Frame", frame)
                cv2.imshow("Road Mask (Height x2)", blank_mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


def main(args=None):
    rclpy.init(args=args)
    node = RoadSegmentNode()
    node.destroy_node()
    rclpy.shutdown()
