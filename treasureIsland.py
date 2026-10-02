left_or_right = input("Welcome to Treasure Island. Your mission is to find the treasure. You are at a cross roads, which path do you take? Left or right? ").lower()
swim_or_wait = input("You come to a river. Do you want to swim across or do you wait? ").lower()
which_door = input("You arrive at the island unharmed. You come across a house with three doors. Which door do you go through? Red, blue or yellow? ").lower()

if left_or_right == "left":
    if swim_or_wait == "wait":
        if which_door == "yellow":
            print("Congratulations! You have found the treasure!")
        elif which_door == "red":
            print("You have been burned by fire. Game Over.")
        elif which_door == "blue":
            print("You have been eaten by beasts. Game Over.")
        else:
            print("You have chosen a door that doesn't exist. Game Over.")
    elif swim_or_wait == "swim":
        print("You have been attacked by a trout. Game Over.")
    else:
        print("You have chosen an option that doesn't exist. Game Over.")
elif left_or_right == "right":
    print("You have fallen into a hole. Game Over.")
else:
    print("You have chosen an option that doesn't exist. Game Over.")