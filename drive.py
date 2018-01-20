import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps


async def forword(robot):
    # 在事件中无法使用？
    await robot.drive_straight(distance_mm(50), speed_mmps(100)).wait_for_completed()


async def backend(robot):
    await robot.drive_straight(distance_mm(-50), speed_mmps(100)).wait_for_completed()

async def left(robot):
    await robot.turn_in_place(degrees(90)).wait_for_completed()

async def right(robot):
    await robot.turn_in_place(degrees(-90)).wait_for_completed()
