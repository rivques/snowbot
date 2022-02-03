# Snowbot
A bot to draw Rocket League snow art. Runs on gcode like a CNC or 3D printer. Currently uses state-setting to travel but might be more intelligent in the future.
## How to set up Cura
This bot uses gcode sliced by [Cura](https://ultimaker.com/software/ultimaker-cura) to run. It must be sliced using Cura so the gcode comments are predictable. Until I get around to adding a .curaprofile, use the settings below to slice an image or model. Even though UE says that 1uu=10cm, this uses 1uu=1mm (in gcode) for simplicity. This will draw the bottom layer.
### Printer settings:
- size: X8192 Y10240
- origin at center
- 1 extruder
- height doesnt matter,should be big
- no heated bed
- marlin flavor
- other settings dont matter
### Profile settings:
- At least one bottome layer
- No bed adhesion
- Walls: (coming soon after experimentation)
## How to draw an image
1. Slice your image/model and save it to disk somewhere. 
2. With RLBot, start a game on a snowy map with only Snowbot, unlimited time, and gravity at super high (helps with infill speed).
3. Select your gcode file with the tkinter interface and press go!
## Statesetting
This bot currently uses statesetting to travel and to move the ball out of the way. If I have the time I will add inteligent movement to jump and aerial from one spot to another.
## 
