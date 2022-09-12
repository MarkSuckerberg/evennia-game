"""
This file should contain every combat-related commands at our disposal.
A finished version of this file should contain:
- The commands to attack/take various action [/] Implemented, not tested
- Damage calculation [X] Unimplemented
- An admin command to spawn weapons [X] Unimplemented
Weapons used in combat are simply checked in the player's inventory
The template/basic weapon is contained in a seperate file called weapon.py
"""

import random
from evennia import Command, CmdSet

class CmdAttack(Command):
    """
    Attack the enemy. Commands:
      hit [<enemy>]
      parry

    hit - Your run of the mill attack
    parry - forgoes your attack but will make you harder to hit on next
            enemy attack.
    """

    # this is an example of implementing many commands as a single
    # command class, using the given command alias to separate between them.

    key = "attack"
    aliases = [
        "hit",
        "kill",
        "fight",
        "defend",
    ]
    locks = "cmd:all()"
    help_category = "Combat"

    def func(self):
        cmdstring = self.cmdstring
        caller = self.caller
        if cmdstring in ("attack", "fight"):
            text = "How do you want to fight? Choose 'hit' or 'defend'."
            caller.msg(text)
            return

        # parry mode
        if cmdstring in ("defend"):
            text = ("You raise your weapon in a defensive pose, ready to block the next enemy attack.")
            caller.msg(text)
            caller.db.combatDefending = True
            caller.location.msg_contents("%s defends!" % caller, exclude=[caller])
            return

        if not self.args:
            caller.msg("Who do you attack?")
            return
        target = caller.search(self.args.strip())
        if not target:
            return

        if cmdstring in ("hit","kill"):
            # the base hit chance in weapons is accessed as:
            # float(self.obj.db.hit)
            hit = .4 + (float(caller.db.power)/10/2)
            # the damage chance in weapons is accessed as:
            # self.obj.db.damage
            damage = 1 + caller.db.power
            string = "You slash with %s. " % self.obj.key
            tstring = "%s slash at you with %s. " % (caller.key, self.obj.key)
            ostring = "%s slash at %s with %s. " % (caller.key, target.key, self.obj.key)
            caller.db.combatDefending = False
        else:
            caller.msg("You fumble with your weapon, unsure of whether to hit or parry ...")
            caller.location.msg_contents("%s fumbles with their weapon." % caller, exclude=caller)
            caller.db.combatDefending = False
            return

        if target.db.combatDefending:
            # checks if the target is parrying/defending
            target.msg("|GYou defend, trying to avoid the attack.|n")
            hit *= 0.55 - (float(caller.db.power)/100*5)

        if random.random() <= hit:
            caller.msg(string + "|gIt's a hit!|n")
            target.msg(tstring + "|rIt's a hit!|n")
            caller.location.msg_contents(ostring + "It's a hit!", exclude=[target, caller])


            #if hasattr(target, "on_hit"):
                # Kept as a possible thing from the gutted tutorial code.
                # Will probably need this for health checks down the line
                #target.on_hit(self.obj, caller, damage)
                #return
            if target.db.currentHp:
                target.db.currentHp -= damage
            else:
                # They lack an hp attribute
                caller.msg("The target seems unaffected.")
                return
        else:
            caller.msg(string + "|rYou miss.|n")
            target.msg(tstring + "|gThey miss you.|n")
            caller.location.msg_contents(ostring + "They miss.", exclude=[target, caller])

class CmdSetCombat(CmdSet):
    def at_cmdset_creation(self):
            self.add(CmdAttack())

"""
From here is a copy paste of the tutorial world's "on hit" code. It still needs to 
be adapted to our needs, ie renaming variables, but this COULD eventually be made
a script that'll be tacked onto players and enemies to handle special effects.
This'll also be neccesary to set death conditions, 
i.e. player respawn or enemy deathgasps.

def at_hit(self, weapon, attacker, damage):
        if self.db.health is None:
            # health not set - this can't be damaged.
            attacker.msg(self.db.weapon_ineffective_msg)
            return

        if not self.ndb.is_immortal:
            if not weapon.db.magic:
                # not a magic weapon - divide away magic resistance
                damage /= self.db.damage_resistance
                attacker.msg(self.db.weapon_ineffective_msg)
            else:
                self.location.msg_contents(self.db.hit_msg)
            self.db.health -= damage

        # analyze the result
        if self.db.health <= 0:
            # we are dead!
            attacker.msg(self.db.death_msg)
            self.set_dead()
        else:
            # still alive, start attack if not already attacking
            if self.db.aggressive and not self.ndb.is_attacking:
                self.start_attacking()
"""