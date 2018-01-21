#!/usr/bin/env python
# encoding: utf-8
import asyncio
import time

import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
import drive
# 同时操作需要使用queue，手动操作loop

drive_map = {
    1:drive.forword,
    2:drive.left,
    3:drive.right,
}

queue = asyncio.Queue()

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
    # await evt.obj._robot.wait_for_all_actions_completed()
    # await drive_map[cube_id](evt.obj._robot)
    await queue.put(cube_id)
    cube.set_lights(cozmo.lights.off_light)
    # 收集完一次执行不会有事件并发的问题。满了之后执行 
    print(dir(queue))
    # print(queue.qsize())

async def worker(robot,queue):
    # consume
    while True:
        qsize = queue.qsize()
        print("qsize:",qsize)
        if qsize >= 1:
            while not queue.empty():
                # wait for an item from the producer
                cube_id = await queue.get()
                # process the item
                print('consuming item {}...'.format(cube_id))
                # simulate i/o operation using sleep
                await drive_map[cube_id](robot)
                await asyncio.sleep(1)
        await asyncio.sleep(1)


async def custom_objects(robot: cozmo.robot.Robot):
    robot.add_event_handler(cozmo.objects.EvtObjectTapped, handle_object_tapped)
    # 拿到loop ._loop
    loop = robot._loop
    # create comumer
    t1 = loop.create_task(worker(robot,queue))
    await t1
    '''
    while True:
        # 逐个运行
        # print(dir(queue))
        print("get:",queue.get())
        time.sleep(0.1)
    '''
# cozmo.robot.Robot.drive_off_charger_on_connect = False  # Cozmo can stay on his charger for this example
# 使用生产者消费者模型 queue
cozmo.run_program(custom_objects, use_3d_viewer=False, use_viewer=False)

