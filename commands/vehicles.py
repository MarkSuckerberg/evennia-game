"""
These vehicle specific commands will be used for
entering vehicles, and disembarking via door objects
"""

from evennia import Command, CmdSet

class CmdEnterVehicle(Command):
    """
    Allows you to enter the vehicle
    
    Usage:
      embark [<vehicle>]

    This should only be accessible when a vehicle
    is in the same area.
    """

    key = "embark"
    aliases = ["embark the", "enter", "enter the"]
    locks = "cmd:cmdLocationCheck()"
    help_category = "Vehicles"
    def parse(self):
        # Snags whatever the targeted vehicle is.
        # Important for 'landing bay' areas.
        self.target = self.args.strip()

    def func(self):
        caller = self.caller
        #if not self.target:
            #Sort of a reminder to consider an error message
            #self.caller.msg("No vehicle found")
            #return
        target = self.obj
        caller.location.msg_contents(f"{caller.key} enters the {target}.")
        caller.move_to(target)


class CmdLeaveVehicle(Command):
    """
    Used to leave a vehicle
 
    Usage:
      disembark

    Works aslong as a VehicleDoorObject is present
    in the same area as the caller.
    """

    key = "disembark"
    aliases = ["exit"]
    locks = "cmd:cmdLocationCheck()"
    help_category = "Vehicles"
    def func(self):
        caller = self.caller
        door = self.obj
        vehicle = door.location
        parent = vehicle.location
        caller.location.msg_contents(f"{caller.key} exits the {vehicle} via the {door}.")
        caller.move_to(parent)

class CmdSetVehicle(CmdSet):
    def at_cmdset_creation(self):
            self.add(CmdEnterVehicle())

class CmdSetDoor(CmdSet):
    def at_cmdset_creation(self):
            self.add(CmdLeaveVehicle())
