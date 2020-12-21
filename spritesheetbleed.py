'''
A simple python script that "bleeds" a sprite sheet (tile map) to fix seam artefacts from caused when rendering tilemaps.

I use this script to fix an issue I had within Unity. 
Even though I use a pixel perfect camera, point filtering, and turned off anti-aliasing, I still occasionally get seam artifacts. 
The only way I could fix this reliably was to "bleed" (pad) the tiles. 

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
'''

import argparse
import imageio as im
import sys

import numpy as np
import matplotlib.pyplot as plt

#sys.argv = ['', '-i', 'tilesheet.png', '-s', '16']

# Optional
parser = argparse.ArgumentParser(description='Sprite sheet bleeder.')
parser.add_argument('-b', '--bleedAmount', help='Input sprite sheet', default=1)

# Required
requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('-i', '--input', help='Input sprite sheet file name', required=True)
requiredNamed.add_argument('-s', '--tileSize', help='Sprite sheet tile size', required=True)
#parser.parse_args(['-h'])

args = parser.parse_args()

FILE_NAME = args.input
TILE_SIZE = int(args.tileSize)
BLEED_AMOUNT = int(args.bleedAmount)

spritesheet_original = im.imread(FILE_NAME)
SPRITESHEET_WIDTH = spritesheet_original.shape[1]
SPRITESHEET_HEIGHT = spritesheet_original.shape[0]

print(FILE_NAME, TILE_SIZE, BLEED_AMOUNT, SPRITESHEET_WIDTH, SPRITESHEET_HEIGHT)

COLUMN_COUNT = int(SPRITESHEET_WIDTH / TILE_SIZE)
ROW_COUNT = int(SPRITESHEET_HEIGHT / TILE_SIZE)
NUMBER_OF_TILES = COLUMN_COUNT * ROW_COUNT

spritesheet_new = np.zeros( (SPRITESHEET_HEIGHT+(((ROW_COUNT-1)*2)*BLEED_AMOUNT) + (BLEED_AMOUNT*2), 
							SPRITESHEET_WIDTH+(((COLUMN_COUNT-1)*2)*BLEED_AMOUNT) + (BLEED_AMOUNT*2),
							spritesheet_original.shape[2]), np.uint8)

TILE_SIZE_PADDED = TILE_SIZE+(BLEED_AMOUNT*2)

nRowBleeds = BLEED_AMOUNT
for row in range(0,ROW_COUNT):
	nColBleeds = BLEED_AMOUNT
	for col in range(0,COLUMN_COUNT):
		# Get the tile from the original tile sheet
		tile = spritesheet_original[row*TILE_SIZE:(row+1)*TILE_SIZE, col*TILE_SIZE:(col+1)*TILE_SIZE, :]

		# Method 1: Copy over the original tile into the new sprite sheet. Do not consider borders.
		#spritesheet_new[(row*TILE_SIZE)+nRowBleeds:((row+1)*TILE_SIZE)+nRowBleeds, (col*TILE_SIZE)+nColBleeds:((col+1)*TILE_SIZE)+nColBleeds, :] = tile
		
		# Method 2 (bleeding): Copy over the original tile into the new sprite sheet. Fill in the new border by repeating the inner pixels.
		tile_padded = np.stack([np.pad(tile[:,:,c], BLEED_AMOUNT, mode='edge') for c in range(tile.shape[2])], axis=2)
		spritesheet_new[(row*TILE_SIZE_PADDED):((row+1)*TILE_SIZE_PADDED),
						(col*TILE_SIZE_PADDED):((col+1)*TILE_SIZE_PADDED), 
						:] = tile_padded

		nColBleeds+=(BLEED_AMOUNT*2)
	nRowBleeds+=(BLEED_AMOUNT*2)

FILE_NAME_OUT = FILE_NAME[:-4]+'_padded.png'
print("Saving:",FILE_NAME_OUT)
im.imwrite(FILE_NAME_OUT, spritesheet_new)


print('Complete.')

