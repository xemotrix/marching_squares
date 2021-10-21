import pygame
import pygame.gfxdraw
from pygame.math import Vector2
from scipy.ndimage import convolve
import numpy as np
import math
import random
import time
WHITE = (255,255,255)

'''
a   b
     
c   d

  e  
f   g  
  h   
'''

spacing = 20

kernel = np.array(
	[[2,2,2],
	[2,1,2],
	[2,2,2]]
)

kernel_ms = np.array(
	[[8, 4], 
	 [1, 2]]
)

gol_map = {
	1  :0,
	3  :0,
	5  :1,
	7  :1,
	9  :0,
	11 :0,
	13 :0,
	15 :0,
	17 :0,
	0  :0,
	2  :0,
	4  :0,
	6  :1,
	8  :0,
	10 :0,
	12 :0,
	14 :0,
	16 :0
}

mapping = {
	0  : [],
	1  : [((1,0),(2,1))],
	2  : [((1,2),(2,1))],
	3  : [((1,0),(1,2))],
	4  : [((0,1),(1,2))],
	5  : [((0,1),(1,0)) , ((1,2),(2,1))],
	6  : [((0,1),(2,1))],
	7  : [((0,1),(1,0))],
	8  : [((0,1),(1,0))],
	9  : [((0,1),(2,1))],
	10 : [((0,1),(1,2)) , ((1,0),(2,1))],
	11 : [((0,1),(1,2))],
	12 : [((1,0),(1,2))],
	13 : [((1,2),(2,1))],
	14 : [((1,0),(2,1))],
	15 : []

}

def distance(point1, point2):
	sqx = (point1[0] - point2[0])**2
	sqy = (point1[1] - point2[1])**2

	return math.sqrt(sqx + sqy)

def draw_aaline(screen, p1, p2, thickness=1):
	center_p = ( (p1[0]+p2[0])/2, (p1[1]+p2[1])/2 )

	length = distance(p1, p2)
	angle = math.atan2(p1[1]-p2[1], p1[0]-p2[0]) 

	UL = (center_p[0] + (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
		center_p[1] + (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
	UR = (center_p[0] - (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
		center_p[1] + (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
	BL = (center_p[0] + (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
		center_p[1] - (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
	BR = (center_p[0] - (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
		center_p[1] - (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))

	vertices = (UL, UR, BL, BR)
	pygame.gfxdraw.aapolygon(screen, vertices, WHITE)
	pygame.gfxdraw.filled_polygon(screen, vertices, WHITE)


def make_mat(mat):

	global kernel
	conv = convolve(mat, kernel)

	h,w = conv.shape

	for i in range(h):
		for j in range(w):
			conv[i,j] = gol_map[conv[i,j]]
	return conv

def get_edge(square):
	global mapping

	lu_value =\
	  square[0][0] * 8 + \
	  square[0][1] * 4 + \
	  square[1][0] * 1 + \
	  square[1][1] * 2

	mapped = mapping[lu_value]
	return mapped


def draw_points(screen, matrix):
	h,w = matrix.shape

	global spacing

	for i in range(h):
		for j in range(w):
			x = (i+1)*spacing
			y = (j+1)*spacing

			color_val = matrix[i][j]*255.0
			color = (color_val, color_val, color_val)

			pygame.draw.circle(screen, color, (x,y), radius=4)


def draw_lines(screen, matrix):
	h,w = matrix.shape

	global spacing

	spacing = 20

	for i in range(h-1):
		for j in range(w-1):
			
			square = matrix[i:i+2, j:j+2]
			edges = get_edge(square)

			x0 = (i+1)*spacing
			y0 = (j+1)*spacing
			half_spacing = int(spacing/2)
			
			for p1,p2 in edges:
				
				x1 = x0 + p1[0]*half_spacing
				y1 = y0 + p1[1]*half_spacing

				x2 = x0 + p2[0]*half_spacing
				y2 = y0 + p2[1]*half_spacing
				
				draw_aaline(screen, (x1, y1), (x2, y2))


if __name__ == '__main__':

	pygame.init()
	clock = pygame.time.Clock()
	infoObject = pygame.display.Info()
	current_w, current_h = infoObject.current_w, infoObject.current_h

	screen = pygame.display.set_mode((current_w,current_h), pygame.FULLSCREEN)

	running = True

	

	matrix = np.random.randint(0,2, (int(current_w/spacing-1), int(current_h/spacing-1)))
	gol_time = 0
	points_time = 0
	lines_time = 0
	counter = 0	
	while running:
		counter += 1
		
		screen.fill((50,50,50))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			else:
				pass
		gol_start = time.time()
		matrix = make_mat(matrix)
		gol_end = time.time()

		points_start = time.time()		
		draw_points(screen, matrix)
		points_end = time.time()

		lines_start = time.time()	
		draw_lines(screen, matrix)
		lines_end = time.time()

		gol_time += gol_end - gol_start
		points_time += points_end - points_start
		lines_time += lines_end - lines_start

		if counter>=30:
			counter = 0

			print('gol',gol_time)
			print('points',points_time)
			print('lines',lines_time)
			gol_time = 0
			points_time = 0
			lines_time = 0

		clock.tick(30)
		pygame.display.update()