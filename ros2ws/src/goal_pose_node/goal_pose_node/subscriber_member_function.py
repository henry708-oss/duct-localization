# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
import graph as g
import pickle
from rclpy.node import Node

from std_msgs.msg import String


class GoalPoseNode(Node):

    def __init__(self, model_name):
        super().__init__('minimal_subscriber')
        super().__init__('minimal_publisher')
        self.subscription = self.create_subscription(
            String,
            'status',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(String, 'goal_pose', 10)

        with open(f"{model_name}.pkl", "rb") as file:
            self.graph = pickle.load(file)
        
        self.distances = g.pathfind(self.graph, self.graph.start)

        self.path = []

    def listener_callback(self, msg):
        data = msg.data.split(",")
        match data[0]:
            case "True":
                goal_pose = self.path.pop()
                msg = String()
                msg.data = f"{goal_pose[0]},{goal_pose[1]},{goal_pose[2]}"
                self.publisher_.publish()
                self.get_logger().info('Publishing: "%s"' % msg.data)
            case "False":
            case _:


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
