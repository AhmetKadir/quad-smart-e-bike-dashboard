Dashboard and Control Unit for Smart Rental Quad Bike

Open and modify bike_designer.ui using QtDesigner.
After making changes, run convert.bat (for Windows).
The dashboard.py file will be automatically updated with the new changes.

Run main.py

On raspberry pi in main_dashboard.py

Change this line:
from src.relay_module import RelayModule

With this:
from src.relay_module_rasp import RelayModule
