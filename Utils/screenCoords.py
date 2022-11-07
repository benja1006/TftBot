def getCoords(coords_file):
    coords = {}
    with open(coords_file) as file:
        for line in file.readlines():
            (key, val) = line.split('=')
            coords[key] = int(val)
    return coords
