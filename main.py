import asyncio
from twitchio.ext import commands, pubsub
import twitchio
import pyjson5
import dolphin_memory_engine
import sys
from functions import create_channel_point_reward, get_broadcaster_id
import math

class App(commands.Bot):
    def __init__(self, token, initial_channels):
        super().__init__(token="oauth:" + token, initial_channels=initial_channels, prefix="!")
        self.client = twitchio.Client(token=token)
        self.client.pubsub = pubsub.PubSubPool(self.client)

        # Load configuration
        with open('config.json5', 'r') as config_file:
            self.config = pyjson5.load(config_file)

        # Register events
        self.register_events()
        dolphin_memory_engine.hook()

        topics = [pubsub.channel_points(self.config["token"])[get_broadcaster_id(self.config["channelName"], self.config["token"])], pubsub.bits(self.config["token"])[get_broadcaster_id(self.config["channelName"], self.config["token"])]]
        self.client.pubsub.subscribe_topics(topics)
    
    def register_events(self):
        @self.event()
        async def event_ready():
            print(f'Logged in as | {self.nick}')
            if "--create" in sys.argv:  # Check if the --create argument is present
                for reward in self.config["rewards"]:
                    if reward["enabled"] == "True":
                        create_channel_point_reward(
                            self.config["channelName"],
                            reward["name"],
                            reward["cost"],
                            self.config["token"],
                            reward["maxPerStream"],
                            reward["maxPerUserPerStream"],
                            reward["cooldown"],
                            reward["maxPerStreamEnabled"],
                            reward["imageSrc"]
                        )

        @self.event()
        async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
            print(f"Bits event: {event}")  # Log bits event
            # do stuff on bit redemptions

        @self.event()
        async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
            print(f'Received channel points event: {event.reward.title}')  # Log the received event
            
            if event.reward.title == self.config["rewards"][0]["name"]:  # Add One Turn
                print('Triggering: Add One Turn')  # Log action
                maxTurns = dolphin_memory_engine.read_bytes(0x8018FCFD, 1)
                maxTurnsPlusOne = int.from_bytes(maxTurns, byteorder='big') + 1
                dolphin_memory_engine.write_bytes(0x8018FCFD, maxTurnsPlusOne.to_bytes(1, byteorder='big'))
                print(f'Max Turns increased to: {maxTurnsPlusOne}')  # Log new max turns

            if event.reward.title == self.config["rewards"][1]["name"]:  # Wipe P1 Items
                print('Triggering: Wipe P1 Items')  # Log action
                dolphin_memory_engine.write_bytes(0x8018FC3D, 0xFFFFFF)

            if event.reward.title == self.config["rewards"][2]["name"]:  # Wipe P2 Items
                print('Triggering: Wipe P2 Items')  # Log action
                dolphin_memory_engine.write_bytes(0x8018FC6D, 0xFFFFFF)

            if event.reward.title == self.config["rewards"][3]["name"]:  # Wipe P3 Items
                print('Triggering: Wipe P3 Items')  # Log action
                dolphin_memory_engine.write_bytes(0x8018FC9D, 0xFFFFFF)

            if event.reward.title == self.config["rewards"][4]["name"]:  # Wipe P4 Items
                print('Triggering: Wipe P4 Items')  # Log action
                dolphin_memory_engine.write_bytes(0x8018FCCD, 0xFFFFFF)

            if event.reward.title == self.config["rewards"][5]["name"]:  # -30 Coins P1
                print('Triggering: -30 Coins P1')  # Log action
                coinP1 = dolphin_memory_engine.read_bytes(0x8018FC54, 2)
                thirtyLostCoinsP1 = int.from_bytes(maxTurns, byteorder='big') - 30
                dolphin_memory_engine.write_bytes(0x8018FC54, thirtyLostCoinsP1.to_bytes(2, byteorder='big'))
                print(f'New Coins P1: {thirtyLostCoinsP1}')  # Log new coin value

            if event.reward.title == self.config["rewards"][6]["name"]:  # -30 Coins P2
                print('Triggering: -30 Coins P2')  # Log action
                coinP2 = dolphin_memory_engine.read_bytes(0x8018FC84, 2)
                thirtyLostCoinsP2 = int.from_bytes(maxTurns, byteorder='big') - 30
                dolphin_memory_engine.write_bytes(0x8018FC54, thirtyLostCoinsP2.to_bytes(2, byteorder='big'))
                print(f'New Coins P2: {thirtyLostCoinsP2}')  # Log new coin value

            if event.reward.title == self.config["rewards"][7]["name"]:  # -30 Coins P3
                print('Triggering: -30 Coins P3')  # Log action
                coinP3 = dolphin_memory_engine.read_bytes(0x8018FCB4, 2)
                thirtyLostCoinsP3 = int.from_bytes(maxTurns, byteorder='big') - 30
                dolphin_memory_engine.write_bytes(0x8018FC54, thirtyLostCoinsP3.to_bytes(2, byteorder='big'))
                print(f'New Coins P3: {thirtyLostCoinsP3}')  # Log new coin value

            if event.reward.title == self.config["rewards"][8]["name"]:  # -30 Coins P4
                print('Triggering: -30 Coins P4')  # Log action
                coinP4 = dolphin_memory_engine.read_bytes(0x8018FC4, 2)
                thirtyLostCoinsP4 = int.from_bytes(maxTurns, byteorder='big') - 30
                dolphin_memory_engine.write_bytes(0x8018FC54, thirtyLostCoinsP4.to_bytes(2, byteorder='big'))
                print(f'New Coins P4: {thirtyLostCoinsP4}')  # Log new coin value

            if event.reward.title == self.config["rewards"][9]["name"]:  # -1 Star P1
                print('Triggering: -1 Star P1')  # Log action
                coinP1 = dolphin_memory_engine.read_bytes(0x8018FC44, 2)
                thirtyLostCoinsP1 = int.from_bytes(maxTurns, byteorder='big') - 1
                dolphin_memory_engine.write_bytes(0x8018FC54, thirtyLostCoinsP1.to_bytes(2, byteorder='big'))
                print(f'New Coins P1: {thirtyLostCoinsP1}')  # Log new coin value

            if event.reward.title == self.config["rewards"][10]["name"]:  # -1 Star P2
                print('Triggering: -1 Star P2')  # Log action
                coinP2 = dolphin_memory_engine.read_bytes(0x8018FC74, 2)
                thirtyLostCoinsP2 = int.from_bytes(maxTurns, byteorder='big') - 1
                dolphin_memory_engine.write_bytes(0x8018FC54, thirtyLostCoinsP2.to_bytes(2, byteorder='big'))
                print(f'New Coins P2: {thirtyLostCoinsP2}')  # Log new coin value

            if event.reward.title == self.config["rewards"][11]["name"]:  # -1 Star P3
                print('Triggering: -1 Star P3')  # Log action
                coinP3 = dolphin_memory_engine.read_bytes(0x8018FCA4, 2)
                thirtyLostCoinsP3 = int.from_bytes(maxTurns, byteorder='big') - 1
                dolphin_memory_engine.write_bytes(0x8018FC54, thirtyLostCoinsP3.to_bytes(2, byteorder='big'))
                print(f'New Coins P3: {thirtyLostCoinsP3}')  # Log new coin value

            if event.reward.title == self.config["rewards"][12]["name"]:  # -1 Star P4
                print('Triggering: -1 Star P4')  # Log action
                coinP4 = dolphin_memory_engine.read_bytes(0x8018FCD4, 2)
                thirtyLostCoinsP4 = int.from_bytes(maxTurns, byteorder='big') - 1
                dolphin_memory_engine.write_bytes(0x8018FC54, thirtyLostCoinsP4.to_bytes(2, byteorder='big'))
                print(f'New Coins P4: {thirtyLostCoinsP4}')  # Log new coin value

            if event.reward.title == self.config["rewards"][13]["name"]:  # Coin Revolution
                print('Triggering: Coin Revolution')  # Log action
                coinP1 = dolphin_memory_engine.read_bytes(0x8018FC34, 2)
                coinP2 = dolphin_memory_engine.read_bytes(0x8018FC64, 2)
                coinP3 = dolphin_memory_engine.read_bytes(0x8018FC94, 2)
                coinP4 = dolphin_memory_engine.read_bytes(0x8018FCC4, 2)
                revParsed = math.floor(int.from_bytes(coinP1, byteorder='big') +
                                         int.from_bytes(coinP2, byteorder='big') + 
                                         int.from_bytes(coinP3, byteorder='big') + 
                                         int.from_bytes(coinP4, byteorder='big') // 4)
                dolphin_memory_engine.write_bytes(0x8018FC34, revParsed.to_bytes(2, byteorder='big'))
                dolphin_memory_engine.write_bytes(0x8018FC64, revParsed.to_bytes(2, byteorder='big'))
                dolphin_memory_engine.write_bytes(0x8018FC94, revParsed.to_bytes(2, byteorder='big'))
                dolphin_memory_engine.write_bytes(0x8018FCB4, revParsed.to_bytes(2, byteorder='big'))
                print(f'New Coins after Revolution: {revParsed}')  # Log new coin value

            if event.reward.title == self.config["rewards"][14]["name"]:  # Star Revolution
                print('Triggering: Star Revolution')  # Log action
                coinP1 = dolphin_memory_engine.read_bytes(0x8018FC44, 2)
                coinP2 = dolphin_memory_engine.read_bytes(0x8018FC74, 2)
                coinP3 = dolphin_memory_engine.read_bytes(0x8018FCA4, 2)
                coinP4 = dolphin_memory_engine.read_bytes(0x8018FCD4, 2)
                revParsed = math.floor(int.from_bytes(coinP1, byteorder='big') +
                                         int.from_bytes(coinP2, byteorder='big') + 
                                         int.from_bytes(coinP3, byteorder='big') + 
                                         int.from_bytes(coinP4, byteorder='big') // 4)
                dolphin_memory_engine.write_bytes(0x8018FC44, revParsed.to_bytes(2, byteorder='big'))
                dolphin_memory_engine.write_bytes(0x8018FC74, revParsed.to_bytes(2, byteorder='big'))
                dolphin_memory_engine.write_bytes(0x8018FCA4, revParsed.to_bytes(2, byteorder='big'))
                dolphin_memory_engine.write_bytes(0x8018FCD4, revParsed.to_bytes(2, byteorder='big'))
                print(f'New Stars after Revolution: {revParsed}')  # Log new star value

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send(f'Hello, {ctx.author.name}!')

if __name__ == "__main__":
    with open('config.json5', 'r') as config_file:
        config = pyjson5.load(config_file)
    
    app = App(token=config["token"], initial_channels=[config["channelName"]])
    app.run()p