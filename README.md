# GCP ArUCo Marker Generator

This is a simple python tool that will help you generate Ground Control Points
markers based on the [ArUCo
specification](https://www.uco.es/investiga/grupos/ava/node/26).

This will create an SVG file, with a real sizing of the image (that is if you
ask the tool to create a marker with a 1000mm side, that's exactly what it will
do).

You then just have to send the corresponding file to a printer if you want it on
a tarp or on a big sticker to make your own GCPs.

Usage is simple and default settings are sane, but things can be customized very
easily.

The complete list is as follows:
```
usage: create_marker.py [-h] [-b] [-c] [--center_alt] [--family]
                        [--family-count 10] [-i 0] [--id-color "darkcyan"]
                        [--margin 50] [-o ./] [-s 500] [--print-id]
                        [-t "4X4_50"] [--watermark "DO NO MOVE"]
                        [--watermark-color "black"]
                        [--watermark-sides "Side String"]
                        [--white-color "white"]

Generates ArUco Markers to be used as Grounds Control Points.
Default configuration is sensible. Output is highly customizable.
This tools creates SVG files that can be sent to a printer immediately.
The size parameter is important.

options:
  -h, --help            show this help message and exit
  -b, --border          Add a border around the marker. Default: False
  -c, --center          Add a center mark to the generated marker. Default:
                        False
  --center_alt          Alternative center mark. Creates a center mark that is
                        not an opposite image of the surrounding pixels.
                        Default: False
  --family              Generate the whole marker family (disregard the chosen
                        id). Default: False
  --family-count 10     Works with --family to generate a specific count of
                        markers from a specific family. The maximum number of
                        markers is defined by the chosen family. Default: None
  -i 0, --id 0          ID of ArUCo tag to generate. Default: 0
  --id-color "darkcyan"
                        Color of the id text (if printed with --print-id). Can
                        be any of the named SVG colors. Default: "darkcyan"
  --margin 50           Side margin in mm. Default: 50
  -o ./, --output ./    Path where the output image containing ArUCo marker
                        will be created. Default: ./
  -s 500, --size 500    Size in mm of the marker to be created. This size does
                        not take into account the margin. Default: 500
  --print-id            Print the id in the corner of the marker. Default:
                        False
  -t "4X4_50", --type "4X4_50"
                        Type of ArUCo tag to generate, one of 4X4_50, 4X4_100,
                        4X4_250, 4X4_1000, 5X5_50, 5X5_100, 5X5_250, 5X5_1000,
                        6X6_50, 6X6_100, 6X6_250, 6X6_1000, 7X7_50, 7X7_100,
                        7X7_250, 7X7_1000, ARUCO_ORIGINAL, APRILTAG_16h5,
                        APRILTAG_25h9, APRILTAG_36h10, APRILTAG_36h11.
                        Default: "4X4_50"
  --watermark "DO NO MOVE"
                        Add a watermark around the marker on the four sides
                        around the marker. Default: None
  --watermark-color "black"
                        Color of the watermark text. Can be any of the named
                        SVG colors. Default: "black"
  --watermark-sides "Side String"
                        Change the watermark on the side of the marker to this
                        string. Default: None
  --white-color "white"
                        Color of the white part of the marker. Can be changed
                        to improve contrast. Can be any of the named SVG
                        colors. Default: "white"

For good size recommendations, please see
http://www.agt.bme.hu/on_line/gsd_calc/gsd_calc.html .
```


## Setup and use
### First installation
```
git clone https://www.github.com/gromain/gcp_aruco_generator
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
./marker_generator.py -c -b --print-id -s 800 --watermark "DO NOT MOVE" --watermark-side "Your Name Here" --margin 100 --family --white-color lightgrey -o ./bache/ --id-color darkslategrey --watermark-color orangered --center_alt
deactivate
```
### Subsequent uses
```
source venv/bin/activate
./marker_generator.py -c -b --print-id -s 800 --watermark "DO NOT MOVE" --watermark-side "Your Name Here" --margin 100 --family --white-color lightgrey -o ./bache/ --id-color darkslategrey --watermark-color orangered --center_alt
deactivate
```



## Inspirations
This project is similar to those others tools (yet different from them) :
https://github.com/dronemapper-io/aruco-geobits
https://github.com/zsiki/Find-GCP
https://github.com/okalachev/arucogen
https://github.com/fdcl-gwu/aruco_generator
https://damianofalcioni.github.io/js-aruco2/
https://github.com/jcmellado/js-aruco
