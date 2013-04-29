import inspect
import random

from asciimap import ascii


class GeographicalFeature(object):

    allowedTransitions = []
    pervasiveness = 0.5

    @classmethod
    def getASCII(klass):
        name = klass.__name__
        return getattr(ascii, name[0].lower() + name[1:])


class Terrain(GeographicalFeature):
    pass


class WaterBody(GeographicalFeature):
    pass


class Plains(Terrain):
    "You are surrounded by grassy plains."
    pervasiveness = 0.8


class Savanna(Plains):
    """
    You are surrounded by grassland mixed with undergrowth and occasional
    trees.
    """


class Woodlands(Savanna):
    "You are in an area of scattered woods and occasional clearings."


class Forest(Woodlands):
    "You are surrounded by trees."


class Jungle(Forest):
    "Wild vegetation lays before you, daunting in its thickness."


class SandyGround(Plains):
    "You are surrounded by sandy ground."
    pervasiveness = 0.3


class RockyGround(Plains):
    "You are surrounded by rocky ground."
    pervasiveness = 0.3


class Hills(RockyGround):
    "You have entered a hilly area."
    pervasiveness = 0.5


class Cliffs(Hills):
    "You face a wall of stone, a cliff too hight to pass unaided."
    pervasiveness = 0.3


class Caves(Hills):
    "You are in an area with caves in the hills."
    pervasiveness = 0.2


class Mountains(Hills):
    "You are in the mountains"
    pervasiveness = 0.4


class AlpineTreeline(Mountains):
    """
    You are in the mountains, below the treeline. You see the occasional
    Krummholz formation.
    """


class HighPeaks(Mountains):
    """
    The wind is blowing hard, and you have a difficult time breathing. You are
    very high up in the mountains, among the highest peaks.
    """
    pervasiveness = 0.2


class HighPlateau(Mountains):
    """
    The wind is blowing hard, and you have a difficult time breathing. You are
    very high up in the mountains, on a large, moderately flat plateau. It is a
    forbidding environment.
    """
    pervasiveness = 0.1


class Valley(Plains):
    "Nestled between the slopes, you are standing in a valley."
    pervasiveness = 0.3


class Ravine(RockyGround):
    """
    You've managed to get yourself into a ravine. Let's see if you can get
    yourself out.
    """
    pervasiveness = 0.3


class Canyon(Ravine):
    """
    You are now in a canyon. A most unenviable position for a traveller to
    be in.
    """
    pervasiveness = 0.3


class Desert(SandyGround):
    """
    You have entered the desert. You wonder how long your water will last if
    you have to keep this up...
    """
    pervasiveness = 0.7


class Buttes(Desert, Hills):
    "Several stunning buttes are within view."
    pervasiveness = 0.1


class Tundra(Desert):
    "As far as you can see in that direction is a frozen wasteland."


class Shoreline(RockyGround):
    """
    You are at the water's edge. The rocky shore might be uncomfortable in
    barefeet.
    """
    pervasiveness = 0.4


class Beach(SandyGround):
    """
    You are on a beach. This would be a lovely place for a vacation. If you
    knew what vacations were.
    """
    pervasiveness = 0.3


class Stream(WaterBody):
    "You are up to your needs in a stream."
    pervasiveness = 0.9


class River(Stream):
    "For some reason, you've decided to take a swim in a river."


class Lake(WaterBody):
    "You are currently in a lake."
    pervasiveness = 0.8


class Ocean(WaterBody):
    "You have entered the ocean."
    pervasiveness = 0.9


# for procedural generation of tile layouts, valid transitions from one tile
# type to another have to be defined.
transitions = {
    Plains: [Plains, SandyGround, RockyGround, Hills, Valley, Desert, Beach,
             Canyon, River, Lake, Ocean, Jungle],
    Woodlands: [Plains, SandyGround, RockyGround, Hills, Valley, Beach,
                Woodlands, Forest, Jungle],
    Hills: [Plains, SandyGround, RockyGround, Hills, Mountains, Canyon, River,
           Lake, Caves],
    Mountains: [Hills, Mountains, HighPlateau, HighPeaks, Valley,
                AlpineTreeline],
    AlpineTreeline: [Mountains, HighPlateau, HighPeaks],
    HighPlateau: [Mountains, HighPlateau, HighPeaks, AlpineTreeline],
    Valley: [Plains, SandyGround, RockyGround, Hills, Mountains, River, Lake],
    Ravine: [Plains, SandyGround, RockyGround, Hills, Ravine, Canyon, River],
    Desert: [Plains, SandyGround, RockyGround, Ravine, Desert, Beach, Canyon,
             River, Lake, Ocean],
    Stream: [Shoreline, River, Stream, Lake],
    Lake: [Plains, SandyGround, RockyGround, Hills, Valley, Desert, Beach,
           River, Lake],
    Ocean: [Shoreline, River, Beach],
    Shoreline: [Ocean, Lake, River, Stream, Shoreline, Beach],
    Tundra: [Ocean, HighPeaks, AlpineTreeline],
    }


transitions[Caves] = transitions[Hills]
transitions[Lake] = transitions[Stream]
transitions[River] = transitions[Stream] + [Beach]
transitions[SandyGround] = transitions[Plains]
transitions[Savanna] = transitions[Plains] + [Savanna, Woodlands]
transitions[Forest] = transitions[Woodlands]
transitions[Jungle] = transitions[Woodlands]
transitions[RockyGround] = transitions[Plains]
transitions[HighPeaks] = transitions[HighPlateau]
transitions[Canyon] = transitions[Ravine]
transitions[Buttes] = transitions[Desert]
transitions[Beach] = transitions[Plains]

# some terrain types require
requires = {
    # each valley tile should be connected to at least two mountains (on each
    # side)
    Valley: [],
    # each river tile should be connected directly to two other river tiles
    River: [],
    # each mountain should have a very high likelihood of having hills as
    # neighbors
    Mountains: [],
    # a beach must have water at least one one side
    Beach: [],
    # A river should be *very* pervasive, but in only distinct directions
    # (primarily usually only two neighbors will have river tiles... sometimes
    # a river will branch, in which case there might be three neigbors (non
    # touching, in that case). Also, where rivers meet oceans, an adjoining
    # tile should be another river tile, to help comprise a river delta.
    River: [],
    }


# the transformation of one terrain type into another would be something that
# occurred with a permanent change (local or global) in temperature (e.g., a
# river turning into a dry ravine).
transforms ={}


def getTileClasses():
    from asciimap import terrain
    classes = inspect.getmembers(terrain, inspect.isclass)
    terrainClasses = [klass for name, klass in classes
        if issubclass(klass, terrain.Terrain)
        and klass is not terrain.Terrain]
    waterClasses = [klass for name, klass in classes
        if issubclass(klass, terrain.WaterBody)
        and klass is not terrain.WaterBody]
    return terrainClasses + waterClasses


def getRandomTileClass():
    # XXX this needs to use the session randomizer... need to move this
    return random.choice(getTileClasses())


def getPassableRandomTileClass():
    tile = getRandomTileClass()
    while not tile.isPassable:
        tile = getRandomTileClass()
    return tile


def getRandomTileTransitionClass(tile, neighborTiles):
    # build sets of all valid transitions for each neighbor, then to find a
    # transition that's valid for them all simultaneously, do an intersection
    if not neighborTiles:
        intersections = transitions[tile]
    elif len(neighborTiles) == 1:
        intersections = neighborTiles
    else:
        intersections = []
        for index, tile in enumerate(neighborTiles):
            if index == len(neighborTiles) - 1:
                break
            thisTransition = transitions[tile]
            nextTransition = transitions[neighborTiles[index + 1]]
            intersections.extend(
                list(set(thisTransition).intersection(nextTransition)))
        # remove redundancies
        intersections = list(set(intersections))
    # the higher tendency the tile is to be pervasive, the more likely the
    # tile will continue being used; if the same tile is not pervaded, randomly
    # select a valid transition tile from the intersections

    # XXX this needs to use the session randomizer... need to move this
    reuseCheck = random.random()
    if tile in intersections and reuseCheck < tile.pervasiveness:
        return tile

    # XXX this needs to use the session randomizer... need to move this
    return random.choice(intersections)
