
import pygame
from collections import deque
from track_barriers import barriers
from improved_car import Car
import csv

# Reorganise the boundary data as walls.
walls = []
for barrier in barriers:
	for i in range(len(barrier)):
		walls.append([barrier[i-1], barrier[i]])

# The main program function.
def main():
	pygame.init()
	WIDTH, HEIGHT = 900, 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	bg = pygame.image.load('track.png')
	bg = pygame.transform.scale(bg, (900, 600))

	# Loading car image and initialising the car object.
	CAR_IMAGE = pygame.image.load('pink_car.png')
	CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (42, 20))
	car1 = Car((100, 150), 0, 2, 6,)
	car1.update(walls)

	# Initialising empty trail list to create a trail for the car.
	trail = deque([], 61)

	drive = False
	show_struct = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					drive = not drive
				if event.button == 3:
					show_struct = not show_struct

		if drive:
			trail.appendleft(car1.pos)
			car1.update(walls, time=1)

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Drawing the car trail. # Make the trail smaller over time...
		if len(trail) < 60:
			for i in range(0, len(trail)):
				pygame.draw.circle(screen, (236, 236-i, 236-3*i), trail[i], i//9)
		else:
			for i in range(0, len(trail)):
				pygame.draw.circle(screen, (236, 236-i, 236-3*i), trail[i], i//9)
			trail.pop()

		# Toggle for showing the rays from the car and the barriers on the map.
		if show_struct:
			for ray in car1.rays:
				pygame.draw.aaline(screen, (255,0,0), ray.pos, ray.terminus)

			for barrier in barriers:
				for i in range(0, len(barrier)):
					pygame.draw.line(screen, (255,255,255), barrier[i-1], barrier[i], 3)

		# Rotating and displaying the car object.
		car_temp = pygame.transform.rotate(CAR_IMAGE, -car1.dir)
		car_rect = car_temp.get_rect()
		car_rect.center = car1.pos
		screen.blit(car_temp, car_rect)
		with open('car_data.csv', 'a') as f:
		      writer = csv.writer(f)
		      writer.writerow([car1.pos, car1.dir, car1.speed])
		
		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()
