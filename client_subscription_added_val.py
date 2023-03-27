import sys

sys.path.insert(0, "..")
import os
# os.environ['PYOPCUA_NO_TYPO_CHECK'] = 'True'

import asyncio
import logging

from asyncua import Client, Node, ua

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger()


class SubscriptionHandler:
    """
    The SubscriptionHandler is used to handle the data that is received for the subscription.
    """

    async def datachange_notification(self, node: Node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """
        _logger.warning('datachange_notification {}'.format(val))


async def main():
    """
    Main task of this Client-Subscription example.
    """
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    namespace = "nsadded"

    client = Client(url=url)
    async with client:
        nsidx = await client.get_namespace_index(namespace)
        # var = await client.nodes.objects.get_child(
        #     [f"{nsidx}:PLC", f"{nsidx}:State"])
        var = await client.nodes.objects.get_child(
            [f"{nsidx}:AddedObj", f"{nsidx}:AddedVal2"])
        handler = SubscriptionHandler()

        # Whether we sleep here or not, the tshark output are the same (3 packets per second), which means that, the packets captured by tshark are the routine between the server the client, while the subscription will not generate extra packets.
        # Hence, the subscription in OPC-UA is the true subscription, not polling.
        # await asyncio.sleep(100000)

        # We create a Client Subscription.
        subscription = await client.create_subscription(100, handler)
        nodes = [var]
        # We subscribe to data changes for one node (variables).
        await subscription.subscribe_data_change(nodes)
        # We let the subscription run for ten seconds
        try:
            while True:
                await asyncio.sleep(10)
        except (KeyboardInterrupt, SystemExit):
            # We delete the subscription (this un-subscribes from the data changes of the two variables).
            # This is optional since closing the connection will also delete all subscriptions.
            await subscription.delete()
            # After one second we exit the Client context manager - this will close the connection.
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
