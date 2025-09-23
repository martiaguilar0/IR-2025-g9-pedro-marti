import random
i=0
while i<20:
    right_value=random.randrange(2,200)
    left_value=random.randrange(2,200)

    print ("Left value: " + str(left_value))
    print ("Right value: " + str(right_value))
    if right_value<40 and left_value<40:
        print ("stop")
    elif left_value<40:
        print ("turn right")
    elif right_value<40:
        print ("turn left")
    else:
        print ("forward")
    i=i+1

