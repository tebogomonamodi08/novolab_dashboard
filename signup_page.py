from nicegui import ui

ui.add_head_html(
    '''
    <style>
    html,body {
    margin:0;
    padding:0;
    height:100%;
    width:100%;
    background-color:black;
    
    }
      </style>
    '''
)

with ui.row().classes('bg-black w-screen h-screen justify-center items-center p-0 m-0'):
    with ui.card().classes('bg-white rounded-xl p-8'):
       with ui.column().classes('items-center space-y-4'):
            with ui.column().classes('justify-center space-y-1'):
                ui.label('Sign in with OTP').classes('font-bold text-xl m-0')
                ui.label('Enter email to get a one time password').classes('-mt-1')
            ui.input(label='Enter email',placeholder='tebogo@novo.com').classes('w-full')
            ui.button('Send OTP').classes('bg-black text-white font-bold').classes('w-full')
            ui.link('Use password instead').classes('text-black text-small')


ui.run()