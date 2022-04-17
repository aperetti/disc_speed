# Disc Speed
This program will record your disc speed in a text file and display it back to you in real time.

The program uses a diff between two frames to find the location of the disc and calculates the speed by referencing the two aruco tags.

![Example Diff](docs/example_diff.png)

## Setup
### Setting up the tap measure
The program expects two aruco tags (seen below). By default the distance between the tags is expected to be 5 feet (center to center).

![Example Setup](docs/example_setup.png)

It's important that the background is static, so that the diffing algorithm doesn't pick up other movement. A wall is the ideal back drop. Shadows have a chance to be picked up depending on the light condition.

