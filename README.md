# SpriteSheetBleed
A simple python script that "bleeds" a sprite sheet (tilemap) to fix seam artefacts that occur when rendering tilemaps.

I used this script to fix an issue I had within Unity. Even though I used a pixel perfect camera, point filtering, and turned off anti-aliasing (among other suggestions I found online), I would still occasionally get seam artifacts. The only way I could fix this reliably was to "bleed" (pad) the tiles. 

Usage:

python spritesheetbleed.py -i tilesheet.png -s 16

For unity, within the sprite editor for a tilemap, slice (Grid by Cell size) settings:

Pixel size = TILE_SIZE

Offset = BLEED_AMOUNT

Padding = BLEED_AMOUNT*2


There is a shell script (using ImageMagick) that I based mine on (I re-implemented in python as I prefer it):

https://charliejwalter.net/spritesheet-bleed/

https://github.com/cjonasw/tile-bleed-margin-generator


Another reference to sprite sheet bleeding:

https://tiled2unity.readthedocs.io/en/latest/fixing-seams/

A nice video that clearly explains the problem in Unity:

https://youtu.be/QW53YIjhQsA
