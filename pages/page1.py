from dashboard import Sidebar
from nicegui import ui


with ui.row():
    Sidebar(ui.notify('Hi'))

ui.run()