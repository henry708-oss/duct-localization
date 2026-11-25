# the central data processing node for drone goal orientation
#
# Authored by Zach Strahan
#
#
# Brain is subscribed to Localizer, goal_pose and status
# Brain publishes a string of the form "BOOL,X,Y,Z"
#




import rclpy
from rclpy.node import Node

class Brain(Node):
    def __init__(self):
        super().__init__('Brain On')
        self.goal_pose = ""
        self.localized = False
        self.pose = ""
        self.diff = ""

        #publishes "BOOL,X,Y,Z"
        self.pose_vec = self.create_publisher(
            #type, 
            #Topic, 
            10
        )

        #publishes "diffX,diffY,diffZ"
        self.drive = self.create_publisher(
            #args1
            #args2,
            10
        )

        self.status = self.create_subscriber(
            #status Node args
        )

        self.local =  self.create_subscriber(
            #locailizer args 
        )

        self.found = self.create_subscriber(
            #localizer args 2
        )

        self.goal = self.create_subscriber(
            #goal_pose args
            self.goal_callback,
            10
        )
        self.timer = self.create_timer(0.1, self.timer_callback)
    

    def goal_callback(self, goal:str):
        target = goal.split(",")
        current = self.pose.split(",") #this has a leading bool value. Pose begins at current[1]
        targetX = float(target[0])
        targetY = float(target[1])
        targetZ = float(target[2])
        curX = float(target[1])
        curY = float(target[2])
        curZ = float(target[3])

        #this should mean the drone will always move toward the correct direction. If cur is bigger than target, we want negative. If target is larger, we want positive
        diffX = targetX-curX
        diffY = targetY-curY
        diffZ = targetZ-curZ

        vector = max(diffX,diffY,diffZ)
        if vector == diffX:
            self.diff = str(diffX)+",0,0"
        elif vector == diffY:
            self.diff = "0,"+str(diffY)+",0"
        elif vector == diffZ:
            self.diff = "0,0,"+str(diffZ) 
               

    def timer_callback(self):
        self.pose_vec.pub(self.pose)
        self.drive.pub(self.diff)



def main(args=None):
    rclpy.init(args=args)
    node = Brain()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()