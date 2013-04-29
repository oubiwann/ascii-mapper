grey = '\033[90m'
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
blue = '\033[94m'
magenta = '\033[95m'
cyan = '\033[96m'
white = '\033[97m'
endColor = '\033[0m'


testTerrain = r"""%s
1234
abcd
56
e
%s
""" % ("noop", "noop")


plains = r"""%s
----
----
--
-
%s
""" % (yellow, endColor)


savanna = r"""%s
-+--
--+-
-+
-
%s
""" % (yellow, endColor)


woodlands = r"""%s
+-++
++-+
+-
+
%s
""" % (green, endColor)


forest = r"""%s
++++
++++
++
+
%s
""" % (green, endColor)


jungle = r"""%s
$+&+
+&+$
&+
&
%s
""" % (green, endColor)


sandyGround = r"""%s
....
....
..
.
%s
""" % (yellow, endColor)


desert = sandyGround
beach = sandyGround


rockyGround = r"""%s
,.,.
.,.,
,.
,
%s
""" % (grey, endColor)


shoreline = rockyGround


hills = r"""%s
^_^_
_^_^
^_
^
%s
""" % (red, endColor)


cliffs = r"""%s
|,,.
.,,|
|,
|
%s
""" % (red, endColor)


caves = r"""%s
^_^_
_O_O
_O
o
%s
""" % (red, endColor)


mountains = r"""%s
^^^^
^^^^
^^
^
%s
""" % (red, endColor)


alpineTreeline = r"""%s
^+^+
+^+^
^+
^
%s
""" % (red, endColor)


highPeaks = r"""%s
/\**
**/\
^*
^
%s
""" % (white, endColor)


highPlateau = r"""%s
/\__
__/\
^_
^
%s
""" % (red, endColor)


valley = r"""%s
\/--
--\/
V-
v
%s
""" % (green, endColor)


ravine = r"""%s
-V-v
v-V-
V-
v
%s
""" % (red, endColor)


canyon = r"""%s
_  _
 \/ 
VV
V
%s
""" % (red, endColor)


buttes = r"""%s
...n
n...
n.
n
%s
""" % (red, endColor)


tundra = r"""%s
*.*.
.*.*
.*
*
%s
""" % (white, endColor)


stream = r"""%s
~S~s
s~S~
~s
~
%s
""" % (cyan, endColor)


river = r"""%s
~{~{
}~}~
~S
~
%s
""" % (cyan, endColor)


lake = r"""%s
~.~.
.~.~
~.
~
%s
""" % (blue, endColor)


ocean = r"""%s
~~~~
~~~~
~~
~
%s
""" % (blue, endColor)


"""
The following ASCII terrain snippets are either old or haven't been used yet.

^\/^
/^^\ Valley (old)

++++
++++

$&$&
&$&$

,.,.
.,., RockyGround (Shoreline)

....
.... SandyGround (Desert/Beach)

====
====

''''
''''

;;;;
;;;;

::::
::::

____
____
"""


large = (1, 3)
large_top = (1, 2)
large_bottom = (2, 3)
medium = (3, 4)
small = (4, 5)


def getTerrain(name, size=large, color=False):
    color_start = ""
    color_end = ""
    name_parts = name.splitlines()
    if color:
        color_start = name_parts[0]
        color_end = name_parts[-1]
    terrain = name_parts[size[0]:size[1]]
    if len(terrain) == 1:
        terrain = [color_start + terrain[0] + color_end]
    elif len(terrain) == 2:
        terrain = [color_start + terrain[0], terrain[1] + color_end]
    return terrain


def printTerrain(name, size=large, color=True):
    print "\n".join(getTerrain(name, size, color))


def getRerrainRow(names, size=large, color=False):
    if size == large:
        result = [
            "".join(map(
                lambda x: getTerrain(x, large_top, color)[0], names)),
            "".join(map(
                lambda x: getTerrain(x, large_bottom, color)[0], names))]
    else:
        result = ["".join(map(
            lambda x: getTerrain(x, size, color)[0], names))]
    return result


def printTerrainRow(names, size=large, color=True):
    print "\n".join(getRerrainRow(names, size, color))


def getTerrainGrid(rows, size=large, color=False):
    return map(lambda x: getRerrainRow(x, size, color), rows)


def printTerrainGrid(rows, size=large, color=True):
    print "\n".join(
        map(lambda x: "\n".join(getRerrainRow(x, size, color)), rows))
