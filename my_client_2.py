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
            ["0:Objects", f"{nsidx}:Arm", f"{nsidx}:Height"])
        value = await var.read_value()
        _logger.info(f"Value of Height ({var}): {value}")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.INFO)
    asyncio.run(main())
