"""
Vehicle Objects are specifically used for objects 
where a character can enter it, exit it, and (possibly)
have some method to drive it, if it's not automatic.

Door code for vehicles is also contained, where they
possess verbs to exit the object to the parent.
"""

from evennia import DefaultObject
from commands.vehicles import CmdSetVehicle
from commands.vehicles import CmdSetDoor

class VehicleObject(DefaultObject):

    def at_object_creation(self):
        # Vehicles will need a script to enter them
        # Without having to use @tel, like we have been
        # And having a door object in the area, seperate
        # Of the ship/loincloth is ineffective.

        self.cmdset.add_default(CmdSetVehicle)


class VehicleDoorObject(DefaultObject):

    def at_object_creation(self):
        # Ideally, I want to have this object in a state
        # Where it can be set down, and be ready for use.

        self.cmdset.add_default(CmdSetDoor)

    def return_appearance(self, looker):
        door = self
        vehicle = door.location
        outside = vehicle.location
        outsideText = super().return_appearance(outside)
        text = super().return_appearance(looker)
        text += "\n" + outsideText
        return text
