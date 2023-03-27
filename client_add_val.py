import asyncio
import logging
import datetime

from asyncua import Client

# To change the objects and namespaces, we should use admin to connect to the server
url = "opc.tcp://admin@localhost:4840/freeopcua/server/"
# namespace = "http://examples.freeopcua.github.io"
namespace = "nsadded"


async def main():
    _logger = logging.getLogger(__name__)
    _logger.warning(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        _logger.warning(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        # var = await client.nodes.root.get_child(
        #     ["0:Objects", f"{nsidx}:PLC", f"{nsidx}:State"])
        var = await client.nodes.root.get_child(
            ["0:Objects", f"{nsidx}:AddedObj", f"{nsidx}:AddedVal"])
        value = await var.read_value()
        _logger.warning(f"Value of AddedVal ({var}): {value}")

        obj = await client.nodes.objects.get_child([f"{nsidx}:AddedObj"])
        value2 = await obj.add_variable(nsidx, "AddedVal2", "adfasf")
        _logger.warning(f"AddedVal2: {value2}")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.WARNING)
    asyncio.run(main())
