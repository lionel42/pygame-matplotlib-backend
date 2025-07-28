# Pygame Matplotlib Backend

Create plots in pygame.


Note that the library is in an experimental developement stage and not
all features of standard matplotlib backends are implement at the moment.

## Installation
```
pip install pygame-matplotlib
```

## Usage

First you will need to specify that you want to use pygame backend.
```python
# Select pygame backend
import matplotlib
matplotlib.use('pygame')
```

Then you can use matplotlib as you usually do.
```python
# Standard matplotlib syntax
import matplotlib.pyplot as plt
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the axes.
plt.show()
```

Or you can include the plot in your game using the fact that a ```Figure``` is
also a ```pygame.Surface``` with this backend.
```python
import pygame
import pygame.display

fig, axes = plt.subplots(1, 1,)
axes.plot([1,2], [1,2], color='green', label='test')

fig.canvas.draw()

screen = pygame.display.set_mode((800, 600))

# Use the fig as a pygame.Surface
screen.blit(fig, (100, 100))

show = True
while show:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Stop showing when quit
            show = False
    pygame.display.update()
```

Note that if you want to update the plot during the game, you might
need to call ```fig.canvas.draw()``` and ```screen.blit(fig)``` during
the game loop.

See examples in test.py or test_show.py


## How it works in the back

The matplotlib ```Figure``` object is replaced by a ```FigureSurface``` object
which inherits from both ```matplotlib.figure.Figure``` and
```pygame.Surface```.


## Current implementation

Support mainly the basic plotting capabilities.

