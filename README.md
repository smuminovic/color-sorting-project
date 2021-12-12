# Color sorting machine

## _Mechatronic system for object sorting based on it's color using Raspberry Pi 3B, Raspberry Pi v2 camera and stepper motor_

Stepper motors and camera, that is attached to microcontroller, are all set on the plastic construction (see figure 2). Objects for sorting, in this case ball-shaped candies are placed in the tube on the top. After starting the system, the camera takes a photo of the first object. After processing the image and determinating the object's color, the lower steper motor (MOTOR 2) turns the slide to one place: 1 - RED. 2 -BLUE, 3 - YELLOW based on the detected color. The first stepper motor (MOTOR 1) rotates the plastic disk located under the tube. The hole on the plastic disk allows the candy to fall on the slide which takes it to the corresponding place. Then the proces repeats.

Tools:
- Python
- Thonny IDE
- Raspbian

## _Schematic/wiring diagram (figure 1)_

![alt text](https://github.com/smuminovic/color-sorting-project/blob/main/shema.png?raw=true)

## _Real system (figure 2)_

![alt text](https://github.com/smuminovic/color-sorting-project/blob/main/system.jpg?raw=true)
