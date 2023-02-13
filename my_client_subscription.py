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
    namespace = "aaaaa"

    client = Client(url=url)
    async with client:
        nsidx = await client.get_namespace_index(namespace)
        # var = await client.nodes.objects.get_child(
        #     [f"{nsidx}:PLC", f"{nsidx}:State"])
        var = await client.nodes.objects.get_child(
            [f"{nsidx}:Arm", f"{nsidx}:Height"])
        handler = SubscriptionHandler()

        # We create a Client Subscription.
        subscription = await client.create_subscription(500, handler)
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
