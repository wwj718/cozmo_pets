#!/usr/bin/env python
# encoding: utf-8
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import time
import drive

drive_map = {
    1:drive.forword,
    2:drive.left,
    3:drive.right,
}


g = 0 # 指令收集到一起 

async def handle_object_tapped(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    # if isinstance(evt.obj, CustomObject)
    global g
    # print(dir(evt.obj._robot))
    print("cube_id:",evt.obj.cube_id) # id不同时各自怎么走
    print("object_id:",evt.obj.object_id)

    cube = evt.obj
    cube.set_lights(cozmo.lights.blue_light)
     # ok
    time.sleep(0.1) # 0.2 
    # cube.set_lights(cozmo.lights.off_light)
    g = g+1
    print("g:",g)

    cube_id = evt.obj.cube_id
    # robot
    await evt.obj._robot.wait_for_all_actions_completed()
    await drive_map[cube_id](evt.obj._robot) 
    cube.set_lights(cozmo.lights.off_light)
    # 收集完一次执行不会有事件并发的问题。满了之后执行 

def custom_objects(robot: cozmo.robot.Robot):
    robot.add_event_handler(cozmo.objects.EvtObjectTapped, handle_object_tapped)
    
    while True:
        time.sleep(0.1)

# cozmo.robot.Robot.drive_off_charger_on_connect = False  # Cozmo can stay on his charger for this example

cozmo.run_program(custom_objects, use_3d_viewer=False, use_viewer=False)

