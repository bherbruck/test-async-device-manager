from device_manager import DeviceManager


def main():
    device_manager = DeviceManager()
    device_manager.on_ready = lambda: print('ready')
    device_manager.on_poll = lambda: print(device_manager.device_ids)
    device_manager.on_connect = lambda device: print(f'{device} connected')
    device_manager.on_disconnect = lambda device: print(
        f'{device} disconnected')

    device_manager.start()


if __name__ == '__main__':
    main()
