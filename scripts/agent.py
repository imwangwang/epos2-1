#!/usr/bin/env python

from epos2.srv import *
import rospy
import sys
import numpy as np
def request_torque(position, current, init=0):
    # print("wait for Service")
    #asset current in range(-2,2)
    rospy.wait_for_service('applyTorque')
    try:
        # print("now request service")
        applyTorque = rospy.ServiceProxy('applyTorque', Torque)
        print("request service: ", current)
        res = applyTorque(position, current, init)
        return res
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def request_init():
    # print("wait for Service")
    rospy.wait_for_service('applyTorque')
    try:
        # print("now request service")
        applyTorque = rospy.ServiceProxy('applyTorque', Torque)
        res = applyTorque(0, 0, 1);
        return res
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [position torque]"%sys.argv[0]

class Env(object):
    def __init__(self, env_name):
        self.name = env_name
        self.action_space = 1
        self.state_space = 3

    def random_action(self):
        return np.random.rand(self.action_space)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        torque = float(sys.argv[1])
        print(type(torque))
        res = request_torque(0, torque)
        print "position_new:", res.position_new, "\tvelocity:", res.velocity, "\treward:", res.reward#, "current:", res.current, 
    else:
        step = 0
        env = Env('Pendulum')
        while(True):
            # init the state by call env.reset(), getting the init state from the service
            # calculate the next move
            # call step service
            step += 1
            # print(env.random_action())
            # rospy.loginfo("request:%s",step)
            # if step % 2:
            #     res = request_torque(step, 10)
            # else:
            #     res = request_torque(step, 20)
            res = request_torque(step, env.random_action()[0]*2-1)
            print "position_new:", res.position_new, "velocity:", res.velocity, "reward:", res.reward#, "current:", res.current, 
            if res.done:
                print("done episode")
                break
            # rospy.loginfo("position_new:%s, velocity:%s, current:%s", res.position_new, res.velocity, res.current)
            # after getting the responce, calc the next move and call step service again