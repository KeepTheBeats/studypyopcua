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
        nsIdx = await client.register_namespace(namespace)
        _logger.warning("Add nsidx {}".format(nsIdx))

        addex_obj = await client.nodes.objects.add_object(nsIdx, "AddedObj")
        _logger.info("addex_obj is {}".format(addex_obj))
        added_var = await addex_obj.add_variable(nsIdx, "AddedVal", "25")
        _logger.info("added_var is {}".format(added_var))
        # Set MyVariable to be writable by clients
        await added_var.set_writable()


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)-15s %(message)s",
                        level=logging.WARNING)
    asyncio.run(main())
