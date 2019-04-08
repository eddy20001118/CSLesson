'''
(C) Yuhao Li 2019
This is a python programme to calculate useful information
of a room by giving width length and height.
bxzr32 2415946
18/01/2019
'''

'''
num_type: type of the number for displaying. Height/Width/Length
maximun: float, maximum number
minium: float, minimum number
default: float, if input is invaild, using the default value
'''

def get_float(num_type, maximum, minium, default):
    #display hint when inputing
    hint = "Input {num_type}, ({minium}-{maximum}), [{default}]: ".format(
        num_type=num_type, minium=minium, maximum=maximum, default=default)
    try:
        #if input is a number, convert to a float number
        user_input = float(input(hint))
        #if input in range, return input
        if user_input>=minium and user_input <=maximum:
            return user_input
        #if input is not in range, return default value
        else:
            print("Input invaild, using default value "+str(default))
            return default
    #if input is not a number, return default
    except:
        print("Input invaild, using default value "+str(default))
        return default

'''
algorithm of room calculation:
volume,base_area,wall_area1,wall_area2
'''
def room_cal():
    # initialise variables
    volume = float(0)       # volume (m^3)
    base_area = float(0)    # area of base (m^2)
    wall_area1 = float(0)
    wall_area2 = float(0)
    
    #get three inputs with given type, maximum, minium and default value
    width = get_float("Width",20,0,10)
    length = get_float("Length",20,0,10)
    height = get_float("Height",20,0,10)

    #put the calculated data into a key-value set
    volume = width * length * height
    base_area = width * length
    wall_area1 = width * height
    wall_area2 = length * height

    #return this key-value set
    return volume,base_area,wall_area1,wall_area2

"""
The entrance of the whole programme.
"""
def main():
    #get the result key value set
    volume,base_area,wall_area1,wall_area2 = room_cal()
    #hint of view answer
    print("View answer(volume, base_area, wall_area1, wall_area2), type Quit to exit")
    #running the loop unless input Quit to break the loop
    while True:
        #input the answer you want to view
        selected_answer = input("option: ")
        #break the while loop is input is Quit, and program will exit
        if selected_answer == "Quit":
            print("Exiting the program")
            break
        elif selected_answer == "volume":
            print(volume)
        elif selected_answer == "base_area":
            print(base_area)
        elif selected_answer == "wall_area1":
            print(wall_area1)
        elif selected_answer == "wall_area2":
            print(wall_area2)
        else:
            print("Invaild input, try again")
"""
To ensure that calling the main function of current file instead of the main function in the imported modules.
"""
if __name__ == "__main__":
    main()
