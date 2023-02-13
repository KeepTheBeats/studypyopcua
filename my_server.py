import asyncio
import logging
import random
import sys

from asyncua import Server


async def main():
    _logger = logging.getLogger(__name__)
    # set up our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # set up our own namespace, not really necessary but should as spec
    # uri = "http://examples.freeopcua.github.io"
    uri = "aaaaa"
    idx = await server.register_namespace(uri)
    _logger.info("idx is {}".format(idx))

    # server.nodes, contains, links to very common nodes like objects and root
    plc_obj = await server.nodes.objects.add_object(idx, "PLC")
    _logger.info("myobj is {}".format(plc_obj))
    state_var = await plc_obj.add_variable(idx, "State", "Good")
    _logger.info("myvar is {}".format(state_var))
    # Set MyVariable to be writable by clients
    await state_var.set_writable()

    # add a new obj, which will be modified by my_client.py and read by my_client_2.py
    new_obj = await server.nodes.objects.add_object(idx, "Arm")
    _logger.info("new_obj: {}".format(new_obj))
    height_var = await new_obj.add_variable(idx, "Height", 100)
    _logger.info("height_var: {}".format(height_var))
    await height_var.set_writable()

    _logger.info("Starting server!")
    async with server:
        try:
            while True:
                sleep_seconds = random.randint(1, 3)
                await asyncio.sleep(sleep_seconds)
                old_val = await state_var.read_value()
                new_val = ""
                if old_val == "Good":
                    new_val = "Bad"
                else:
                    new_val = "Good"
                _logger.info("Set value of %s to %s", state_var, new_val)
                await state_var.write_value(new_val)
        except (KeyboardInterrupt, SystemExit):
            server.stop()
            sys.exit()


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.DEBUG)
    asyncio.run(main(), debug=True)
