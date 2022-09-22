import asyncio
from dataclasses import dataclass, field
import random
from typing import Callable, List, TypeVar


T = TypeVar('T')
NoneCallback = TypeVar('NoneCallback', bound=Callable[[], None])
DeviceCallback = TypeVar('DeviceCallback', bound=Callable[[str], None])

none_callback: NoneCallback = lambda: None
device_callback: DeviceCallback = lambda _: None


def random_ids(ids=['a', 'b', 'c', 'd'], max_length=3) -> List[str]:
    return random.sample(ids, random.randint(0, max_length))


@dataclass
class DeviceManager:
    on_ready: NoneCallback = none_callback
    on_poll: NoneCallback = none_callback
    on_connect: DeviceCallback = device_callback
    on_disconnect: DeviceCallback = device_callback
    polling_interval: int = 1
    _device_ids: List[str] = field(repr=False, default_factory=list)
    _new_device_ids: List[str] = field(repr=False, default_factory=list)

    @property
    def device_ids(self) -> List[str]:
        return self._device_ids

    def start(self, interval: int = None):
        loop = asyncio.get_event_loop()
        loop.create_task(self._poll(interval or self.polling_interval))
        loop.create_task(self.test())
        self.on_ready()
        loop.run_forever()

    def stop(self):
        loop = asyncio.get_event_loop()
        loop.stop()

    async def test(self):
        while True:
            self._new_device_ids = random_ids()
            await asyncio.sleep(random.randint(1, 5))

    async def _poll(self, interval: int):
        while True:
            self.on_poll()

            for device in self._device_ids:
                if device not in self._new_device_ids:
                    self.on_disconnect(device)
                    self.device_ids.remove(device)

            for device in self._new_device_ids:
                if device not in self._device_ids:
                    self.on_connect(device)
                    self.device_ids.append(device)

            await asyncio.sleep(interval)
