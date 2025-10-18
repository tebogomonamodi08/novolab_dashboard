from nicegui import ui


@ui.page('/dashboard', title='Dashboard')
def dashboard_view():
    ui.label('Hey, This is you dashboard.')