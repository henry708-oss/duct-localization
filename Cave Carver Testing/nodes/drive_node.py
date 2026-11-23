#Drive node for publishing velocity commands
# 
# Authored by Zach Strahan
#
#
# Drive_Node subscribes to Brain and receives a string that it converts into velocity commands
#


#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from mrs_msgs.msg import VelocityReferenceStamped # we need this for the drone


class Drive_Node(Node):
    def __init__(self):
        super().__init__('DriverVelocity')
        self.cur_cmd = VelocityReferenceStamped()
        topic = f'/{self.uav_name}/control_manager/velocity_reference' # needed by MRS_UAV
        self.pub = self.create_publisher(
            VelocityReferenceStamped, 
            topic, 
            10) # from MRS_msgs, needed by MRS_UAV

        # Publish at 20 Hz (0.05s) so ControlManager does not time out. Needed by MRs_UAV
        self.timer = self.create_timer(0.05, self.timer_callback)
        
        self.brain_subscriber = self.create_subscription(
            #MSGTYPE, String of "x,y,z" global frame
            #Topic, Something like "pose"
            self.brain_callback, 
            10
        )
        self.get_logger().info("Driver started")

    #format of VelocityReferenceStamped struct taken from AI summary
    def brain_callback(self, #MSGTYPE
                       ):
        #logic for converting incoming string from brain to a velocity command. Essentially sets Velocity Referenced Stamped
        self.cur_cmd.header.stamp = self.get_clock().now().to_msg()
        # Use '{uav_name}/fcu_untilted' for horizontal body-frame velocity,
        # or '{uav_name}/world_origin' / '{uav_name}/local_origin' for world frame
        self.cur_cmd.header.frame_id = f'{self.uav_name}/world_origin'

        #EDIT WITH CORRECT TYPES
        msg = MSG.split(",")

        # Linear velocity (m/s)
        self.cur_cmd.reference.velocity.x = float(msg[0])   # Forward
        self.cur_cmd.reference.velocity.y = float(msg[1])   # Left
        self.cur_cmd.reference.velocity.z = float(msg[2])   # Up

        # Optional: hold a fixed altitude instead of using velocity.z
        self.cur_cmd.reference.use_altitude = False
        self.cur_cmd.reference.altitude = 3.0

        # Heading control: set either use_heading OR use_heading_rate to True
        self.cur_cmd.reference.use_heading = False
        self.cur_cmd.reference.heading = 0.0          # rad

        self.cur_cmd.reference.use_heading_rate = False
        self.cur_cmd.reference.heading_rate = 0.2     # rad/s (counter-clockwise yaw)
    

    #essentiall a while loop for updating the velocity commands
    def timer_callback(self):
        self.pub.publish(self.cur_cmd)


def main(args=None):
    rclpy.init(args=args)
    node = Drive_Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()