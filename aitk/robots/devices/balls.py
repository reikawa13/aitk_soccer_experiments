import math

from ..utils import distance, rotate_around, intersect, distance_point_to_line
from .base import BaseDevice

from aitk.utils import Color


class Ball(BaseDevice): 
    """
    New implementation of a ball class
    """

    def __init__(self, x=0, y=0, name=None, world=None, **kwargs):
        config = {
            "x": x,
            "y": y,
            "name": name,
        }
        config.update(kwargs)
        self.radius = 6
        self._watcher = None
        self.robot = None
        self.world = world
        self.from_json(config)
        self.vx = 0 # the x velocity of the ball
        self.vy = 0 # the y velocity of the ball
        self.friction = 0.1
        self.goal = False

    def initialize(self):
        """
        Internal method to set all settings to default values.
        """
        self.type = "ball"
        self.dist_from_center = distance(0, 0, self._x, self._y)
        self.dir_from_center = math.atan2(-self._x, self._y)


    def to_json(self):
        """
        Save the internal settings to a config dictionary.
        """
        config = {
            "class": self.__class__.__name__,
            "color": str(self.color),
            "x": self._x,
            "y": self._y,
            "name": self.name,
        }
        return config
    
    def from_json(self, config):
        """
        Set the settings from a device config.

        Args:
            config (dict): a config dictionary
        """
        valid_keys = set(["x", "y", "name", "color", "class"])
        self.verify_config(valid_keys, config)

        if "x" in config:
            self._x = config["x"]
        if "y" in config:
            self._y = config["y"]

        if "name" in config:
            name = config["name"]
        else:
            name = None
        self.name = name if name is not None else "ball"

        if "color" in config:
            self.color = Color(config["color"])
        else:
            self.color = Color("orange")
        self.initialize()
    

    #NOT SURE WHAT THESE DO...
    @property
    def x(self):
        if self.robot is None:
            return self._x
        else:
            if self.dist_from_center != 0:
                x, y = rotate_around(0,
                                     0,
                                     self.dist_from_center,
                                     self.robot.a + self.dir_from_center)
                return x
            else:
                return 0

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        if self.robot is None:
            return self._y
        else:
            if self.dist_from_center != 0:
                x, y = rotate_around(0,
                                     0,
                                     self.dist_from_center,
                                     self.robot.a + self.dir_from_center)
                return y
            else:
                return 0
            
    def get_position(self, world=True):
        """
        Get the relative or global position of the device.

        Args:
            world (bool): if True, return the global coordinates of the
                device. Otherwsie, return the local, relative position.
        """
        if self.robot is None:
            return self._x, self._y
        else:
            if world:
                if self.dist_from_center != 0:
                    x, y = rotate_around(self.robot.x,
                                         self.robot.y,
                                         self.dist_from_center,
                                         self.robot.a + self.dir_from_center)
                    return x, y
                else:
                    return self.robot.x, self.robot.y
            else: # local to robot
                if self.dist_from_center != 0:
                    x, y = rotate_around(0,
                                         0,
                                         self.dist_from_center,
                                         self.robot.a + self.dir_from_center)
                    return x, y
                else:
                    return 0, 0
                

    @y.setter
    def y(self, value):
        self._y = value

    def __repr__(self):
        return "<Ball x=%r, y=%r, name=%r>" % (self._x, self._y, self.name)
    
    def _step(self, time_step):
        """
        Have the ball move one step in time. Check to see if it hits
        any obstacles.
        """
        old_x, old_y = self.x, self.y 
        new_x, new_y = self.x + self.vx, self.y + self.vy

        if not self.goal and self.world is not None:
            self.goal = self._if_goal(old_x, old_y, new_x, new_y)
        if not self.goal:
            self.x, self.y = self._bounce_if_needed(old_x, old_y, new_x, new_y)
  
        # update the velocity while preventing backward movement
        if self.vx > 0:
            self.vx = max(0, self.vx - self.friction)
        else:
            self.vx = min(0, self.vx + self.friction)
        if self.vy > 0:
            self.vy = max(0, self.vy - self.friction)
        else:
            self.vy = min(0, self.vy + self.friction)   

    def _bounce_if_needed(self, old_x, old_y, new_x, new_y):
        """
        if ball hits left/right coundary, vx reverses
        if ball hits top/bottom boundary: vy reverses
        only do this when going into the wall
        returns: new_x and new_y, updates self.vx, self.vy
        """
        left = self.radius
        right = self.world.width - self.radius
        top = self.radius
        bottom = self.world.height - self.radius

        if new_x < left and self.vx < 0:
            new_x = left 
            self.vx = -self.vx 
        elif new_x > right and self.vx > 0:
            new_x = right
            self.vx = -self.vx
        
        if new_y < top and self.vy < 0:
            new_y = top
            self.vy = -self.vy
        elif new_y > bottom and self.vy > 0:
            new_y = bottom
            self.vy = -self.vy

        return new_x, new_y
    
        for wall in self.world._walls:
            if wall.wtype != "boundary":
                continue
            for line in wall.lines:
                distance, _ = distance_point_to_line((new_x, new_y), line.p1, line.p2)
                if distance <= self.radius:
                    if line.p1.x == line.p2.x:
                        self.vx = -self.vx
                    elif line.p1.y == line.p2.y:
                        self.vy = -self.vy
                    return old_x, old_y
        return new_x, new_y

    def _if_goal(self, old_x, old_y, new_x, new_y):
        for wall in self.world._walls:
            if wall.wtype != "wall":
                continue
            for line in wall.lines:
                if intersect(old_x, old_y, new_x, new_y, 
                             line.p1.x, line.p1.y, line.p2.x, line.p2.y):
                    self.vx = 0
                    self.vy = 0
                    return True
        return False


    def impact_from_robot(self, robot, degrees, robot_velocity, strength=3.0):
        """
        Called when a robot hits the ball to push it away from the robot. 
        - calculate the direction of where the ball will be(dx, dy) 
        - get the velocity gap between the robot and the ball
        - add the velocity gap to the ball speed
        """
        # impact direction
        dx, dy = self.x - robot.x, self.y - robot.y 
        distance = math.sqrt(dx**2+dy**2)
        print("distance is", distance)
        if distance == 0:
            return
        norm_dx, norm_dy = dx/distance, dy/distance
        # print(dx, dy)
        # print(robot_vx, robot_vy)

        # impact strength
        robot_wvx = robot_velocity * math.cos(math.radians(degrees))
        robot_wvy = robot_velocity * (-math.sin(math.radians(degrees)))
        vgap_x, vgap_y =  robot_wvx - self.vx, robot_wvy - self.vy
        print(vgap_x, vgap_y)

        impact_speed = vgap_x * norm_dx + vgap_y * norm_dy

        self.vx += norm_dx * impact_speed * strength
        self.vy += norm_dy * impact_speed * strength

        print(self.vx, self.vy)





    def impact(self, x, y):
        """
        Receives impact signals from the robots. 
        Updates the x_velcity and y_velocity.
        """
        self.vx = x
        self.vy = y

    def update(self, draw_list=None):
        """
        Update the device.

        Args:
            draw_list (list): optional. If given, then the
                method can add to it for drawing later.
        """
        draw_list.append(("strokeStyle", (Color(255), 1)))
        draw_list.append(("draw_cirlce", (self.x, self.y, self.radius)))
        draw_list.append("noStroke")
        

    def draw(self, backend):
        """
        Draw the device on the backend.

        Args:
            backend (Backend): an aitk drawing backend
        """
        x, y = self.get_position(world=True)
        backend.set_fill(self.color)
        backend.strokeStyle(Color("black"), 1)
        backend.draw_circle(x, y, self.radius)
        backend.noStroke()

    def watch(self, title="Bulb:"):
        """
        Create a dynamically updating view
        of this device.

        Args:
            title (str): title of device
        """
        widget = self.get_widget(title=title)
        return display(widget)


    def get_widget(self, title="Bulb:"):
        """
        Return the dynamically updating widget.

        Args:
            title (str): title of device
        """
        from ..watchers import AttributesWatcher

        if self.robot is None or self.robot.world is None:
            print("ERROR: can't watch until added to robot, and robot is in world")
            return None

        if self._watcher is None:
            self._watcher = AttributesWatcher(
                self, "name", "brightness", title=title, labels=["Name:", "Brightness:"]
            )
            self.robot.world._watchers.append(self._watcher)

        return self._watcher.widget
