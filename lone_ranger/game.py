#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player
from zombie import Zombie
from overlay import Overlay
import random

"""This file is garbage. It was a hastily coded mockup
to demonstrate how to use the engine.  We will be creating
a Game class that organizes this code better (and is
reusable).
"""

# Function to call when colliding with zombie

def main():
    
    e = league.Engine("The Lone Ranger")
    e.init_pygame()

    sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
    t = league.Tilemap('./assets/world.lvl', sprites, layer = 1)
    b = league.Tilemap('./assets/background.lvl', sprites, layer = 0)
    world_size = (t.wide * league.Settings.tile_size, t.high * league.Settings.tile_size)
    
    e.drawables.add(t.passable.sprites())
    e.drawables.add(b.passable.sprites())
    
    p = Player(2, 400, 300)
    o = Overlay(p)
    p.blocks.add(t.impassable)
    p.world_size = world_size
    p.rect = p.image.get_rect()
    
    e.drawables.add(p)
    
    e.drawables.add(o)
    
    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size)
    
    e.objects.append(c)
    e.objects.append(o)

    
    #need to register more collisions with new zombie here
    
    #Register events?
    pygame.time.set_timer(pygame.USEREVENT + 0, 250// league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT + 1, 500 // league.Settings.gameTimeFactor)
 
    #Player movements

    e.key_events[pygame.K_a] = p.move
    e.key_events[pygame.K_d] = p.move
    e.key_events[pygame.K_w] = p.move
    e.key_events[pygame.K_s] = p.move
    
     def spwanZombies(time):
        listx = [0, 0, 400, 800]
        listy = [0, 300, 0, 300]
        randomInt = random.randint(0,3)
        if random.randint(1,100) > 75:
            z = Zombie(p, 10, listx[randomInt], listy[randomInt])
            e.drawables.add(z)
            e.objects.append(z)
            #z.blocks.add(t.impassable)
            e.collisions[z] = (p, p.ouch)

    def updateZoms(time):
        for i in e.objects:
            if isinstance(i,Zombie) and random.randint(1,100) > 50:
                    i.move_towards_player(time)  
        e.objects.remove(c)
        e.objects.append(c) 
        print(len(e.objects))    
    
    #Register zombie movements in event list
    e.events[pygame.USEREVENT] = updateZoms
    e.events[pygame.USEREVENT + 1] =  spwanZombies
    #e.events[pygame.USEREVENT + 1] = q.move_right
    #e.events[pygame.USEREVENT + 2] = q.move_up
    #e.events[pygame.USEREVENT + 3] = q.move_down
    
    
    #Sets up exit button to quit game
    e.events[pygame.QUIT] = e.stop
    
    
    #Runs the main game loop
    e.run()

    

if __name__=='__main__':
    main()
