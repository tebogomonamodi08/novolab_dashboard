from nicegui import ui

ui.add_body_html('''
<style>
    html, body {
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden;
    }
    
    .nicegui-content {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .q-radio .q-option {
        margin-bottom: 0.10rem !important;
    }
</style>
''')

class Sidebar:
    def __init__(self):
        self._build()

    def _build(self):
        with ui.column().classes('bg-black items-center text-white h-screen w-1/5 top-0 left-0 m-0 p-0'):
            ui.label('Management').classes('font-bold')
            options = ['Campaigns','Areas', 'Campaign Schedules','Search']
            x='Campaigns'
            
            with ui.column().classes('gap-y-0 items-start w-full'):
                for opt in options:
                    button_class = 'text-xs hover:bg-gray-800 w-full rounded '+('bg-white/10 text-black' if opt==x else 'bg-black')
                    with ui.row().classes('mb-0 pt-0 pb-0 hover-grey justify-center w-full'):
                        ui.button(opt).classes(button_class)

sidebar = Sidebar()

ui.run()