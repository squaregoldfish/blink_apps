#!/usr/bin/python3
import os, time

########################################################
##
## CONFIGURATION

# Define the colors to use for different load levels
# Define them in ascending order. Otherwise things will be weird.
scaledef = [
    {
    "load": 0,
    "color": [0, 0, 255]
    },
    {
    "load": 8,
    "color": [0, 255, 0]
    },
    {
    "load": 12,
    "color": [255, 255, 0]
    },
    {
    "load": 16,
    "color": [255, 0, 0]
    }
  ]

blinkcmd = "blink1-tool -q"

##########################################################
##
## FUNCTIONS
def _getload():
  return os.getloadavg()[0]


def _setblink(rgb):
  cmd = blinkcmd + " --rgb=" + str(rgb[0]) + "," + str(rgb[1]) + "," + str(rgb[2])
  os.system(cmd)

def _interpolatecolor(color1, color2, proportion):
  return round(color1 + (color2 - color1) * proportion)


def _getloadcolor(load):

  result = [128, 128, 128]

  if load <= scaledef[0]["load"]:
    result = scaledef[0]["color"]
  elif load >= scaledef[-1]["load"]:
    result = scaledef[-1]["color"]
  else:

    preventry = None
    nextentry = None

    for i in range(0, len(scaledef)):
      if scaledef[i]["load"] == load:
        preventry = scaledef[i]
        nextentry = scaledef[i]
      elif scaledef[i]["load"] < load and scaledef[i + 1]["load"] > load:
        preventry = scaledef[i]
        nextentry = scaledef[i + 1]




    if preventry["color"] == nextentry["color"]:
      result = preventry["color"]
    else:
      colorproportion = (load - preventry["load"]) / (nextentry["load"] - preventry["load"])
      redvalue = _interpolatecolor(preventry["color"][0], nextentry["color"][0], colorproportion)
      greenvalue = _interpolatecolor(preventry["color"][1], nextentry["color"][1], colorproportion)
      bluevalue = _interpolatecolor(preventry["color"][2], nextentry["color"][2], colorproportion)

      result = [redvalue, greenvalue, bluevalue]



  return result


###################################################
##
## MAIN
def main():
  while True:
    load = _getload()
    color = _getloadcolor(load)
    _setblink(color)
    time.sleep(15)



if __name__ == '__main__':
  main()
