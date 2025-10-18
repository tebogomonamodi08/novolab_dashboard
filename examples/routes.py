'''
we use decorators to define a new page instance in nicegui, with the following argument:
1. path
2.title
'''
from nicegui import ui

name = 'Tebogo'
@ui.page('/dark/{name}',title='Darkpage', dark=True)
def dark(name):
    ui.label(f'Hey There {name}')
    ui.link('Back','/')

@ui.page('/')
def main():
    ui.link('dark page', f'dark/{name}')

ui.run()