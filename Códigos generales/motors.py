from ideaboard import IdeaBoard

ib = IdeaBoard()

# motor speed is from -1.0 (reverse) to 1.0 (forward)
# 0 is stopped with brake, None = roll freely
ib.motor_1.throttle = 1.0
ib.motor_2.throttle = -1.0