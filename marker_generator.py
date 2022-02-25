#!/bin/python3

# Copyright (c) 2022 Romain Bazile
#
# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import svgwrite
import json
import argparse
import cv2
import sys, os

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
    "4X4_50": cv2.aruco.DICT_4X4_50,
    "4X4_100": cv2.aruco.DICT_4X4_100,
    "4X4_250": cv2.aruco.DICT_4X4_250,
    "4X4_1000": cv2.aruco.DICT_4X4_1000,
    "5X5_50": cv2.aruco.DICT_5X5_50,
    "5X5_100": cv2.aruco.DICT_5X5_100,
    "5X5_250": cv2.aruco.DICT_5X5_250,
    "5X5_1000": cv2.aruco.DICT_5X5_1000,
    "6X6_50": cv2.aruco.DICT_6X6_50,
    "6X6_100": cv2.aruco.DICT_6X6_100,
    "6X6_250": cv2.aruco.DICT_6X6_250,
    "6X6_1000": cv2.aruco.DICT_6X6_1000,
    "7X7_50": cv2.aruco.DICT_7X7_50,
    "7X7_100": cv2.aruco.DICT_7X7_100,
    "7X7_250": cv2.aruco.DICT_7X7_250,
    "7X7_1000": cv2.aruco.DICT_7X7_1000,
    "ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11,
}


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
Generates ArUco Markers to be used as Grounds Control Points.
Default configuration is sensible. Output is highly customizable.
This tools creates SVG files that can be sent to a printer immediately.
The size parameter is important.""",
    epilog="For good size recommendations, please see http://www.agt.bme.hu/on_line/gsd_calc/gsd_calc.html .",
)
ap.add_argument(
    "-b",
    "--border",
    action="store_true",
    help="Add a border around the marker. Default: False",
)
ap.add_argument(
    "-c",
    "--center",
    action="store_true",
    help="Add a center mark to the generated marker. Default: False",
)
ap.add_argument(
    "--center_alt",
    action="store_true",
    help="Alternative center mark. Creates a center mark that is not an opposite image of the surrounding pixels. Default: False",
)
ap.add_argument(
    "--family",
    action="store_true",
    help="Generate the whole marker family (disregard the chosen id). Default: False",
)
ap.add_argument(
    "--family-count",
    type=int,
    default=None,
    metavar=10,
    help="Works with --family to generate a specific count of markers from a specific family. The maximum number of markers is defined by the chosen family. Default: None",
)
ap.add_argument(
    "-i",
    "--id",
    type=int,
    default=0,
    metavar=0,
    help="ID of ArUCo tag to generate. Default: 0",
)
ap.add_argument(
    "--id-color",
    type=str,
    default="darkcyan",
    metavar='"darkcyan"',
    help='Color of the id text (if printed with --print-id). Can be any of the named SVG colors. Default: "darkcyan"',
)
ap.add_argument(
    "--margin",
    type=int,
    default=50,
    metavar=50,
    help="Side margin in mm. Default: 50",
)
ap.add_argument(
    "-o",
    "--output",
    type=str,
    default="./",
    metavar="./",
    help="Path where the output image containing ArUCo marker will be created. Default: ./",
)
ap.add_argument(
    "-s",
    "--size",
    type=int,
    default=500,
    metavar=500,
    help="Size in mm of the marker to be created. This size does not take into account the margin. Default: 500",
)
ap.add_argument(
    "--print-id",
    action="store_true",
    help="Print the id in the corner of the marker. Default: False",
)
ap.add_argument(
    "-t",
    "--type",
    type=str,
    default="4X4_50",
    metavar='"4X4_50"',
    help=f"Type of ArUCo tag to generate, one of {', '.join(list(ARUCO_DICT.keys()))}. Default: \"4X4_50\"",
)
ap.add_argument(
    "--watermark",
    type=str,
    default=None,
    metavar='"DO NO MOVE"',
    help="Add a watermark around the marker on the four sides around the marker. Default: None",
)
ap.add_argument(
    "--watermark-color",
    type=str,
    default="black",
    metavar='"black"',
    help='Color of the watermark text. Can be any of the named SVG colors. Default: "black"',
)
ap.add_argument(
    "--watermark-sides",
    type=str,
    default=None,
    metavar='"Side String"',
    help="Change the watermark on the side of the marker to this string. Default: None",
)
ap.add_argument(
    "--white-color",
    type=str,
    default="white",
    metavar='"white"',
    help='Color of the white part of the marker. Can be changed to improve contrast. Can be any of the named SVG colors. Default: "white"',
)
args = vars(ap.parse_args())

markersize = args["size"]
dict_name = args["type"]
marker_id = args["id"]
output_folder = args["output"]
white_color = args["white_color"]
watermark_color = args["watermark_color"]
id_color = args["id_color"]
border = 1 if args["border"] else 0
margin_mm = args["margin"]
alternate = args["center_alt"]

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if ARUCO_DICT.get(dict_name, None) is None:
    print(f"ArUCo tag of {dict_name} is not supported")
    sys.exit(1)
else:
    # load the ArUCo dictionary
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[dict_name])

if not os.path.exists(output_folder):
    # create the path!
    os.makedirs(output_folder)
if args["family"]:
    filepath = f"{output_folder}{dict_name}/"
    if not os.path.exists(filepath):
        # create the path!
        os.makedirs(filepath)
else:
    filepath = f"{output_folder}{dict_name}_"


datawidth = arucoDict.markerSize

pixsize_mm = markersize / (datawidth + border * 2)

margin = margin_mm / pixsize_mm

pixcount = datawidth + border * 2 + margin * 2

imagesize = round(pixsize_mm * pixcount)

print(f"Total marker size is going to be {imagesize}mm")


def addCenterMark(svg, circle_rad, pixcount, bits, datawidth, white_color, alternate):
    # svg.add(svg.circle(center=(pixcount / 2, pixcount / 2), r=circle_rad, fill="red"))
    if alternate:
        # an alternate target was requested, mark is black and white
        return alternate_center_mark(svg, circle_rad, pixcount, "white")

    if bits[1 * datawidth + 1] + bits[2 * datawidth + 1] + bits[
        2 * datawidth + 2
    ] + bits[1 * datawidth + 2] in [0, 4]:
        # all 4 bits are the same color, mark color is the opposite of the chosen colors
        return alternate_center_mark(svg, circle_rad, pixcount, white_color)

    pixels_group = svg.g()
    col = "black" if bits[1 * datawidth + 1] else white_color
    pixels_group.add(
        svg.path(
            d=f"M{pixcount / 2} {pixcount / 2-circle_rad} A {circle_rad} {circle_rad} 0 0 0 {pixcount / 2-circle_rad} {pixcount / 2} L {pixcount / 2} {pixcount / 2}",
            fill=col,
        )
    )
    col = "black" if bits[2 * datawidth + 1] else white_color
    pixels_group.add(
        svg.path(
            d=f"M{pixcount / 2 - circle_rad} {pixcount / 2} A {circle_rad} {circle_rad} 0 0 0 {pixcount / 2} {pixcount / 2+circle_rad} L {pixcount / 2} {pixcount / 2}",
            fill=col,
        )
    )
    col = "black" if bits[2 * datawidth + 2] else white_color
    pixels_group.add(
        svg.path(
            d=f"M{pixcount / 2} {pixcount / 2+circle_rad} A {circle_rad} {circle_rad} 0 0 0 {pixcount / 2+circle_rad} {pixcount / 2} L {pixcount / 2} {pixcount / 2}",
            fill=col,
        )
    )
    col = "black" if bits[1 * datawidth + 2] else white_color
    pixels_group.add(
        svg.path(
            d=f"M{pixcount / 2 + circle_rad} {pixcount / 2} A {circle_rad} {circle_rad} 0 0 0 {pixcount / 2} {pixcount / 2-circle_rad} L {pixcount / 2} {pixcount / 2}",
            fill=col,
        )
    )
    return pixels_group


def alternate_center_mark(svg, circle_rad, pixcount, white_color):
    pixels_group = svg.g()
    pixels_group.add(
        svg.path(
            d=f"M{pixcount / 2} {pixcount / 2-circle_rad} A {circle_rad} {circle_rad} 0 0 0 {pixcount / 2-circle_rad} {pixcount / 2} L {pixcount / 2} {pixcount / 2}",
            fill=white_color,
        )
    )
    pixels_group.add(
        svg.path(
            d=f"M{pixcount / 2 - circle_rad} {pixcount / 2} A {circle_rad} {circle_rad} 0 0 0 {pixcount / 2} {pixcount / 2+circle_rad} L {pixcount / 2} {pixcount / 2}",
            fill="black",
        )
    )
    pixels_group.add(
        svg.path(
            d=f"M{pixcount / 2} {pixcount / 2+circle_rad} A {circle_rad} {circle_rad} 0 0 0 {pixcount / 2+circle_rad} {pixcount / 2} L {pixcount / 2} {pixcount / 2}",
            fill=white_color,
        )
    )
    pixels_group.add(
        svg.path(
            d=f"M{pixcount / 2 + circle_rad} {pixcount / 2} A {circle_rad} {circle_rad} 0 0 0 {pixcount / 2} {pixcount / 2-circle_rad} L {pixcount / 2} {pixcount / 2}",
            fill="black",
        )
    )
    return pixels_group


def createPixels(svg, bits, datawidth, border, margin, white_color):
    pixels_group = svg.g()
    for i in range(datawidth):
        for j in range(datawidth):
            color = white_color if bits[i * datawidth + j] else "black"
            if not border or color == white_color:
                pixels_group.add(
                    svg.rect(
                        insert=(j + border + margin, i + border + margin),
                        size=(1, 1),
                        fill=color,
                        stroke=color,
                        stroke_width=0.0001,
                    )
                )
    return pixels_group


def addId(svg, margin, pixcount, id_color, marker_id):
    pixels_group = svg.g()
    id_position = (margin + margin / 8, pixcount - margin - margin / 8)
    pixels_group.add(
        svg.text(
            f"{marker_id}",
            insert=id_position,
            fill=id_color,
            text_anchor="start",
            font_size=f"{margin*0.7}",
            font_weight="bold",
            font_family="Inter",
        )
    )
    pixels_group.add(
        svg.text(
            f"{marker_id}",
            insert=id_position,
            fill=id_color,
            text_anchor="start",
            font_size=f"{margin*0.7}",
            font_weight="bold",
            font_family="Inter",
            transform=f"rotate(180 {pixcount / 2} {pixcount / 2})",
        )
    )
    return pixels_group


def generate_marker(marker_id):
    bytes = arucoDict.bytesList[marker_id][0]
    bits = []
    bitsCount = datawidth * datawidth
    # Parse marker's bytes
    for byte in bytes:
        start = bitsCount - len(bits)
        bits.extend(((byte >> i) & 1) for i in range(min(7, start - 1), -1, -1))

    svg = svgwrite.Drawing(
        f"{filepath}{marker_id}.svg",
        profile="full",
        viewBox=f"0 0 {pixcount} {pixcount}",
        xmlns="http://www.w3.org/2000/svg",
        size=(f"{imagesize}mm", f"{imagesize}mm"),
        shape_rendering="crispEdges",  # disable anti-aliasing to avoid little gaps between rects
    )
    # background
    svg.add(
        svg.rect(
            (0, 0),
            (pixcount, pixcount),
            fill="white",
        )
    )

    # Border if necessary
    if border:
        svg.add(
            svg.rect(
                (margin, margin),
                (datawidth + border * 2, datawidth + border * 2),
                fill="black",
            )
        )

    svg.add(createPixels(svg, bits, datawidth, border, margin, white_color))

    circle_diam_mm = 10
    circle_rad = circle_diam_mm / pixsize_mm / 2
    if args["center"]:
        svg.add(
            addCenterMark(
                svg, circle_rad, pixcount, bits, datawidth, white_color, alternate
            )
        )

    if args["print_id"]:
        svg.add(addId(svg, margin, pixcount, id_color, marker_id))

    watermark_position = (pixcount / 2, pixcount - margin / 8)
    font_size = f"{margin*0.9}"
    font_weight = "bold"
    font_family = "Inter"
    if args["watermark"]:
        svg.add(
            addWatermarkTop(
                svg,
                watermark_position,
                font_size,
                font_weight,
                font_family,
                args["watermark"],
            )
        )
    if args["watermark_sides"] or args["watermark"]:
        svg.add(
            addWatermarkSides(
                svg,
                watermark_position,
                font_size,
                font_weight,
                font_family,
                args["watermark_sides"] or args["watermark"],
            )
        )

    svg.save()


def addWatermarkSides(
    svg, watermark_position, font_size, font_weight, font_family, watermark_text
):
    pixels_group = svg.g()
    pixels_group.add(
        svg.text(
            f"{watermark_text}",
            insert=watermark_position,
            fill=watermark_color,
            text_anchor="middle",
            font_size=font_size,
            font_weight=font_weight,
            font_family=font_family,
            transform=f"rotate(90 {pixcount / 2} {pixcount / 2})",
            textLength=pixcount - margin * 2,
            lengthAdjust="spacingAndGlyphs",
        )
    )
    pixels_group.add(
        svg.text(
            f"{watermark_text}",
            insert=watermark_position,
            fill=watermark_color,
            text_anchor="middle",
            font_size=font_size,
            font_weight=font_weight,
            font_family=font_family,
            transform=f"rotate(270 {pixcount / 2} {pixcount / 2})",
            textLength=pixcount - margin * 2,
            lengthAdjust="spacingAndGlyphs",
        )
    )
    return pixels_group


def addWatermarkTop(
    svg, watermark_position, font_size, font_weight, font_family, watermark_text
):
    pixels_group = svg.g()
    pixels_group.add(
        svg.text(
            f"{watermark_text}",
            insert=watermark_position,
            fill=watermark_color,
            text_anchor="middle",
            font_size=font_size,
            font_weight=font_weight,
            font_family=font_family,
            textLength=pixcount - margin * 2,
            lengthAdjust="spacingAndGlyphs",
        )
    )
    pixels_group.add(
        svg.text(
            f"{watermark_text}",
            insert=watermark_position,
            fill=watermark_color,
            text_anchor="middle",
            font_size=font_size,
            font_weight=font_weight,
            font_family=font_family,
            transform=f"rotate(180 {pixcount / 2} {pixcount / 2})",
            textLength=pixcount - margin * 2,
            lengthAdjust="spacingAndGlyphs",
        )
    )
    return pixels_group


if args["family"]:
    if args["family_count"]:
        if args["family_count"] > len(arucoDict.bytesList):
            print(
                f"The chosen family count ({args['family_count']}) is bigger than the available markers in the chosen dictionary ({len(arucoDict.bytesList)})."
            )
            print(
                f"The the marker count will be limited to {len(arucoDict.bytesList)}."
            )
            marker_count = len(arucoDict.bytesList)
        else:
            print(
                f"You chose to create {args['family_count']} markers. Those can be found in the folder {filepath} ."
            )
            marker_count = args["family_count"]
    else:
        print(
            f"You chose to create {len(arucoDict.bytesList)} markers. Those can be found in the folder {filepath} ."
        )
        marker_count = len(arucoDict.bytesList)
    for marker_id in range(marker_count):
        generate_marker(marker_id)
else:
    print(
        f"Your marker has been created and is available here {filepath}{marker_id}.svg ."
    )
    generate_marker(marker_id)
