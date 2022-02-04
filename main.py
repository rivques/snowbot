from numpy import arctan
from gcodeinstruction import GcodeInstruction
from util import routines, tools, utils
from util.agent import Vector, VirxERLU, game_object, run_bot
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator
import logging
import re
class Bot(VirxERLU):
    def init(self):
        # NOTE This method is ran only once, and it's when the bot starts up
        self.logger = logging.getLogger("SNOWBOT")
        self.logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)
        self.logger.info("Snowbot init!")
        self.layer_end_re = re.compile(r"^G(1|0)(?=.*Z(\d+(\.\d*)))", flags=re.IGNORECASE)
        
    def load_gcode(self, filepath):
        layer_started = False
        self.logger.info(f"Loading gcode file {filepath}...")
        self.instructions = []
        with open(filepath) as f:
            for i, line in enumerate(f.readlines()):
                line = line.strip()
                layer_mo = self.layer_end_re.match(line)
                if not layer_started and layer_mo and layer_mo.group(2) == "0.2":
                    layer_started = True
                    self.logger.info(f"First line of layer found (#{i+1}): {line}")
                    continue
                if not layer_started:
                    continue
                if layer_mo and layer_mo.group(2) == "0.4":
                    self.logger.info(f"Last line of layer found (#{i+1}): {line}")
                    break
                self.instructions.append(GcodeInstruction(line, i))
        
        self.current_instruction = None
        self.current_instruction_num = -1
        self.current_gcode_type = None

    def run(self):
        # NOTE This method is ran every tick
        if len(self.friends) > 0 or len(self.enemies) > 0:
            self.logger.warn("There are other cars on the field!")
        if self.is_clear():
            # time for the next instruction
            self.current_instruction_num += 1
            self.current_instruction = self.instructions[self.current_instruction_num]
            while not self.current_instruction.valid:
                self.current_instruction_num += 1
                self.current_instruction = self.instructions[self.current_instruction_num]
            if self.current_instruction.type is not None:
                self.current_gcode_type = self.current_instruction.type
            elif self.current_instruction.is_travel:
                car_state = CarState(physics=Physics(location=Vector3(self.current_instruction.y,self.current_instruction.y, None)))
                game_state = GameState(cars={self.index: car_state})
                self.set_game_state(game_state)
            else:
                # get a rotator pointing toward our destination
                angle = arctan((self.me.location.y - self.current_instruction.y)/(self.me.location.x - self.current_instruction.x))
                # point us that way
                car_state = CarState(physics=Physics(rotation=Rotator(0, angle, 0)))
                game_state = GameState(cars={self.index: car_state})
                self.set_game_state(game_state)
                # go there
                self.push(routines.goto(Vector(self.current_instruction.x, self.current_instruction.y), brake=True))


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
