
from pyModbusTCP.client import ModbusClient
c = ModbusClient(host="127.0.0.1", port=502, unit_id=1, auto_open=True)

while True:
    x = input()
    c.write_single_register(1, int(x))

