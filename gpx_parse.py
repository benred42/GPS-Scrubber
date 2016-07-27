import argparse
import math

import gpxpy
import gpxpy.gpx


def main(filepath, max_dist, output_file):
    with open(filepath, 'r') as gpx_file:

        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            previous_point = track.segments[0].points[0]
            for segment in track.segments:
                if segment.points:
                    points = segment.points
                    index = 0
                    for point in points:
                        if point.distance_2d(previous_point) > float(max_dist):
                            segment.remove_point(index)
                        else:
                            previous_point = point
                            index += 1

        with open(output_file, 'w+') as dest:
            dest.write(gpx.to_xml())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'GPX File Scrubber')
    parser.add_argument('filepath',
                        help='The path to the gpx file to be scrubbed'
                        )
    parser.add_argument('max_dist',
                        help='The maximum distance between points, in meters'
                        )
    parser.add_argument('output_file',
                        help='The path to the file to be written with the output'
                        )
    args = parser.parse_args()
    main(sys.argv[1], sys.argv[2])
