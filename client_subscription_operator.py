import asyncio
import logging
import random
import time

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
        var = await client.nodes.objects.get_child(
            [f"{nsidx}:Arm", f"{nsidx}:Height"])
        while True:
            value = await var.read_value()
            if value > 100:
                value = 1
            await var.write_value(value + 1)
            sleep_seconds = random.randint(1, 3)
            time.sleep(sleep_seconds)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.INFO)
    asyncio.run(main())
