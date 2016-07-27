import argparse
import math

import gpxpy
import gpxpy.gpx

# Parsing an existing file:
# -------------------------

def bearing(origin, destination):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `origin: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `destination: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(origin) != tuple) or (type(destination) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(origin[0])
    lat2 = math.radians(destination[0])

    diffLong = math.radians(destination[1] - origin[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return round(compass_bearing, 2)

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
                            print('DISTANCE: ' +
                            str(round(point.distance_2d(previous_point), 2)) +
                            'm BEARING: ' +
                            str(bearing(previous_coord, current_coord)) +
                            ' degrees')

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
