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

    def parse(self):
        # Snags whatever the targeted vehicle is.
        # Important for 'landing bay' areas.
        target = self.caller.search(self.args.lstrip())
        if not target:
            #Sort of a reminder to consider an error message
            #But i don't know if parse will flip its shit
            #with an actual command in it
            #self.caller.msg("No vehicle found")
            raise InterruptCommand()


    def func(self):
        caller = self.caller

        target = caller.search(self.target)
        caller.location.msg_contents(f"{caller.key} enters the {target}.")

        caller.move_to(train)


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

    def func(self):
        # The next 3 lines are just shamelessly
        # Stolen from the train tutorial, given
        # That they work just fine.
        train = self.obj
        parent = train.location
        self.caller.move_to(parent)

class CmdSetVehicle(CmdSet):
    def at_cmdset_creation(self):
            self.add(CmdEnterVehicle())
            self.add(CmdLeaveVehicle())