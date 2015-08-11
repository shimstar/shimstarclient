# shimstarclient

This project is a part of Shimstar Project. This is the user's client project.
The client is written in python.

I use this following library:
-- Panda3d : 3d graphical engine
-- Cegui : famous GUI engine

# Shimstar

Shimstar is an indie mmo space game. Purpose is to create X-Wing like game, I like dog fighting like this.
I hope to have missions, sand boxing, and so on....

## Installation

Shimstar use panda3d as graphical engine (http://www.panda3d.org/).
Shimstar use pyCegui as Ui manager (https://pypi.python.org/pypi/PyCEGUI/0.7.5 --> python 2.7)

To run, shimstar needs ressource (Cegui ressources, models, sounds, pictures,...). Grab it from github (https://github.com/shimstar/shimstarupdater/tree/master/ressources)

## Configuration

All you need is to configure config.xml, with the ressource directory, and the ip of the server.

## Code Source description

main.py contains an event dispatcher, and will start some thread:
- mainserver network to contact main server
- zoneserver, zone and gameinspace if user is into a zone

shimstar/core : constantes and common stuff between station and space game

shimstar/game : stuff for play in space (gameinspace will handle all things about play (movement, shoot,...), UI management

shimstar/gui : stuff about management of game windows

    - system : game start on connection, character choose, and load game
    - game : window during game (inventory, targeting,...)
    - station : window into the station (merchant, fitting, ...)

shimstar/items : classes concerning item

shimstar/network

shimstar/npc

shimstar/user

shimstar/world/zone  :  zone is managing all network communication concerning user playing, npc, and different event to play the game.

# Chat 

Join us on https://shimstar.slack.com 

[![Stories in Ready](https://badge.waffle.io/shimstar/shimstarclient.png?label=ready&title=Ready)](http://waffle.io/shimstar/shimstarclient)
