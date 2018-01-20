# test.py
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
import cozmo
import time 

cube1 = robot.world.get_light_cube(LightCube1Id)  # looks like a paperclip
cube2 = robot.world.get_light_cube(LightCube2Id)  # looks like a lamp / heart
cube3 = robot.world.get_light_cube(LightCube3Id)  # looks like the letters 'ab' over 'T'

#颜色
cube2.set_lights(cozmo.lights.blue_light)

cube2.set_lights(cozmo.lights.blue_light)
cube2.set_lights(cozmo.lights.off_light)



import asyncio

# queue = asyncio.Queue()

def handle_object_tapped(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    # if isinstance(evt.obj, CustomObject)
    # global g
    print("evt run")
    print(dir(evt.obj))
    print("cube_id:",evt.obj.cube_id) # id不同时各自怎么走
    print("object_id:",evt.obj.object_id)

    cube = evt.obj
    cube.set_lights(cozmo.lights.blue_light)
    import time # ok
    time.sleep(1) # 0.2 # 逐个执行没问题 使用queue
    # asyncio queue 的问题
    cube.set_lights(cozmo.lights.off_light)
    # print(g)
    # 收集到一个地方
    # print("Cozmo started seeing a %s" % str(evt.obj.object_type))


# 事件 tapped
# http://cozmosdk.anki.com/docs/generated/cozmo.objects.html#cozmo.objects.EvtObjectTapped
robot.add_event_handler(cozmo.objects.EvtObjectTapped, handle_object_tapped)