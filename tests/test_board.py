import sys
import types
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Provide lightweight stubs for optional runtime modules so the Board class
# can be imported in a test environment.
if "RPi" not in sys.modules:
    rpi_module = types.ModuleType("RPi")
    gpio_module = types.ModuleType("RPi.GPIO")
    gpio_module.BOARD = 10
    gpio_module.IN = 0
    gpio_module.PUD_UP = 1
    gpio_module.BOTH = 0
    gpio_module.input = lambda pin: 1
    gpio_module.setup = lambda *args, **kwargs: None
    gpio_module.setmode = lambda *args, **kwargs: None
    gpio_module.wait_for_edge = lambda *args, **kwargs: None
    rpi_module.GPIO = gpio_module
    sys.modules["RPi"] = rpi_module
    sys.modules["RPi.GPIO"] = gpio_module

if "netifaces" not in sys.modules:
    netifaces_module = types.ModuleType("netifaces")
    netifaces_module.ifaddresses = lambda iface: {2: [{"addr": "127.0.0.1"}]}
    sys.modules["netifaces"] = netifaces_module

from app import Board as board_module
from app.Board import Board


class TestBoard(unittest.TestCase):
    def test_check_alert_repeats_every_ten_minutes_for_one_hour(self):
        board = Board.__new__(Board)
        board._Board__pin = 17
        board._Board__ip = "127.0.0.1"
        board._Board__input_status = 1
        board._Board__board_logger = Mock()

        event = Mock()
        start_time = datetime(2024, 1, 1, 12, 0, 0)
        times = [
            start_time,
            start_time + timedelta(minutes=10),
            start_time + timedelta(minutes=20),
            start_time + timedelta(minutes=30),
            start_time + timedelta(minutes=40),
            start_time + timedelta(minutes=50),
            start_time + timedelta(minutes=55),
            start_time + timedelta(hours=1),
        ]

        with patch.object(board_module, "datetime") as mock_datetime, \
             patch.object(board_module, "sleep", return_value=None), \
             patch.object(board_module.GPIO, "input", return_value=1):
            mock_datetime.now.side_effect = times
            board.check_alert(event)

        self.assertEqual(event.alert.call_count, 6)


if __name__ == "__main__":
    unittest.main()
