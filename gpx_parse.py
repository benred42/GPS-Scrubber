import math

import gpxpy
import gpxpy.gpx

# Parsing an existing file:
# -------------------------

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371000 # m

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return round(d, 2)

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

def main():
    with open('xml_data.txt', 'r') as gpx_file:

        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                if segment.points:
                    points = segment.points[1:]
                    previous_point = segment.points[0]
                    index = 1
                    for point in points:
                        previous_coord = (previous_point.latitude, previous_point.longitude)
                        current_coord = (point.latitude, point.longitude)
                        print('DISTANCE: ' + str(distance(previous_coord, current_coord)) + 'm BEARING: ' + str(bearing(previous_coord, current_coord)) + ' degrees')
                        if distance(previous_coord, current_coord) > 50:
                            segment.remove_point(index)
                        else:
                            previous_point = point
                        index += 1
        with open('scrubbed.gpx', 'w+') as dest:
            dest.write(gpx.to_xml())

if __name__ == '__main__':
    main()
