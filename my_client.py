import asyncio
import logging

from asyncua import Client

url = "opc.tcp://localhost:4840/freeopcua/server/"
# namespace = "http://examples.freeopcua.github.io"
namespace = "aaaaa"


async def main():
    _logger = logging.getLogger(__name__)
    _logger.info(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        _logger.info(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        # var = await client.nodes.root.get_child(
        #     ["0:Objects", f"{nsidx}:PLC", f"{nsidx}:State"])
        var = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:PLC", f"{nsidx}:State"])
        value = await var.read_value()
        _logger.info(f"Value of MyVariable ({var}): {value}")

        new_val = ""
        if value == "Good":
            new_val = "Bad"
        else:
            new_val = "Good"
        _logger.info(f"Setting value of PLC.State to {new_val} ...")
        await var.write_value(new_val)

        # modify a new variable, which is read by my_client_2.py
        height_var = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:Arm", f"{nsidx}:Height"])
        height_val = await height_var.read_value()
        _logger.info("height_var: {}, value: {}".format(
            height_var, height_val))
        await height_var.write_value(height_val * 2)
        _logger.info("Write height_var: {} as value: {}".format(
            height_var, height_val * 2))


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.INFO)
    asyncio.run(main())
