from util import routines, tools, utils
from util.agent import Vector, VirxERLU, run_bot
import logging
import re


class Bot(VirxERLU):
    # If the bot encounters an error, VirxERLU will do it's best to keep the bot from crashing.
    # VirxERLU uses a stack system for it's routines. A stack is a first-in, last-out system of routines.
    # VirxERLU on VirxEC Showcase -> https://virxerlu.virxcase.dev/
    # Questions? Want to be notified about VirxERLU updates? Join my Discord -> https://discord.gg/5ARzYRD2Na
    # Wiki -> https://github.com/VirxEC/VirxERLU/wiki
    def init(self):
        # NOTE This method is ran only once, and it's when the bot starts up
        self.logger = logging.getLogger("SNOWBOT")
        self.logger.setLevel(logging.DEBUG)

        self.layer_end_re = re.compile(r"^G(1|0)(?=.*Z(\d+(\.\d*)))", flags=[re.IGNORECASE])
        self.line_re = re.compile(r"^G(1|0)(?=.*x(\d+(\.\d*)))(?=.*y(\d+(\.\d*))).*", flags=[re.IGNORECASE])
        self.type_re = re.compile(r";TYPE:(.*)", flags=[re.IGNORECASE])
    
    def load_gcode(filepath):
        layer_started = False
        self.logger.info(f"Loading gcode file {filepath}...")
        with open(filepath) as f:
            for line in f.readlines():
                layer_mo = self.layer_end_re.match(line)
                if not layer_started and layer_mo and int(layer_mo.group(2)) == 0.2:
                    layer_started = True
                    self.logger.info(f"First line of layer found: {line}")
                    continue
                if layer_mo and int(layer_mo.group(2)) == 0.4:
                    self.logger.info(f"Last line of layer found: {line}")
                    break
                    

    def run(self):
        # NOTE This method is ran every tick
        if len(self.friends) > 0 or len(self.enemies) > 0:
            self.logger.warn("There are other cars on the field!")
        

    def demolished(self):
        # NOTE This method is ran every tick that your bot it demolished

        # If the stack isn't clear
        if not self.is_clear():
            # Clear the stack
            self.clear()

    def handle_tmcp_packet(self, packet):
        super().handle_tmcp_packet(packet)

        self.print(packet)

    def handle_match_comm(self, msg):
        # NOTE This is for handling any incoming match communications

        # All match comms are Python objects
        if msg.get('team') is self.team:
            self.print(msg)

    def handle_quick_chat(self, index, team, quick_chat):
        # NOTE This is for handling any incoming quick chats

        # See https://github.com/RLBot/RLBot/blob/master/src/main/flatbuffers/rlbot.fbs#L376 for a list of all quick chats
        if self.team is team:
            self.print(quick_chat)


if __name__ == "__main__":
    run_bot(Bot)
