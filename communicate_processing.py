from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import asyncio

"""
This is an example class on how to communicate with processing. It is based on the open sound control protocol.
This protocol just provides use with convenient libraries and a standardized communicatie template.
It is stable and fast and can send almost anything you want in terms of floats, lists, ints, strings. 
It is accompanied by communicate_python.pde on the processing side. 

to install run: pip install python-osc
"""


class OSC:
    def __init__(self):
        # IP address, if you want to communicate with a device on the same network, you probably need to change stuff here.
        # especially differentiate between the PC and the device IP. However, this allows you to run processing on android
        # but do optimization on desktop and still have wireless communication.

        self.ip = "127.0.0.1"

        # the port we receive data from processing on
        self.receiving_port = 12001

        # the port where processing expects data to be send.
        self.sending_port = 12000

        # OSC works with addresses. Basically we can filter on the incoming address and have different handler based on an address.
        # in a case we dont recoginize the address, we use the default handler.
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/filter", self.print_handler)
        self.dispatcher.map("/quit", self.quit_handler)
        self.dispatcher.set_default_handler(self.default_handler)

        # the client we use for sending data.
        self.sending_client = SimpleUDPClient(
            self.ip, self.sending_port
        )  # Create client

        # a boolean to see whether we need to quit the server based on incoming messages.
        self.run = True

    def send_message(self, address, message, verbose=True):
        # send a message to processing.
        # adress needs to be a string.

        self.sending_client.send_message(address, message)
        if verbose:
            print(f"send {message} to {address}")

    # the different handlers. You can easily add your own here, and add them to the dispatcher.
    def print_handler(self, address, *args):
        print(f"{address}: {args}")

    def quit_handler(self, address, *args):
        print("QUITING")
        self.run = False

    def default_handler(self, address, *args):
        print(f"DEFAULT {address}: {args}")

    # This is the main loop, anything you wanna do, you should do it in here.
    # If you are doing time intensive stuff, you need to start thinking about threading
    # because anything you do in here blocks receiving new messages.
    async def loop(self):
        direction_x = 10
        direction_y = 10
        max_x = 400 - direction_y
        max_y = 400 - direction_y
        x = 0
        y = 0
        size = 10
        size_step = 1
        max_size = 30
        min_size = 10
        while self.run:
            # ------ DO YOUR STUFF HERE ------- #
            # move rect

            if x > max_x or x < 0:
                print()
                direction_x *= -1
                y += direction_y
                osc.send_message("y", y)

            if y > max_y or y < 0:
                direction_y *= -1

            if size < min_size or size > max_size:
                size_step *= -1

            size += size_step

            x += direction_x
            osc.send_message("x", x)
            osc.send_message("w", size)
            osc.send_message("h", size)

            #
            # # other stuff
            # osc.send_message("/test/int", 1)
            # osc.send_message("/test/float", 1.1)
            # osc.send_message("/test/list", [1, 2, 3, 4])
            # osc.send_message("/test/arbitrary/stuff", [1, 2.3, 3.1415, "hello world"])

            await asyncio.sleep(
                0.1
            )  # we need some time to process whether we have incoming data.

    # setup a non-blocking receiving server.
    async def init_main(self):
        server = AsyncIOOSCUDPServer(
            (self.ip, self.receiving_port), self.dispatcher, asyncio.get_event_loop()
        )
        (
            transport,
            protocol,
        ) = (
            await server.create_serve_endpoint()
        )  # Create datagram endpoint and start serving
        await self.loop()  # Enter main loop of program
        transport.close()  # Clean up serve endpoint

    # start everything
    def start(self):
        asyncio.run(self.init_main())


if __name__ == "__main__":
    osc = OSC()
    osc.start()
