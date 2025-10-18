from nicegui import ui
from authentication_controller import send_otp

#------Global Variables-----------
email_field = None
otp_button = None
otp_field=None


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
       with ui.column().classes('items-center space-y-3'):
            with ui.column().classes('justify-center space-y-1'):
                ui.label('Sign in with OTP').classes('font-bold text-xl m-0')
                ui.label('Enter email to get a one time password').classes('-mt-1')
            email_field = ui.input(label='Enter email',placeholder='tebogo@novo.com').classes('w-full')

            #------Send OTP handler------------
            def handle_otp():
                success = send_otp(email_field.value)
                if success:
                    ui.notify('OTP Sent, Check you email',color='green')
                    otp_button.props(remove='disabled')
                    otp_field.props(remove='disabled')
            
                
            ui.button('Send OTP', on_click=handle_otp).classes('bg-black text-white font-bold').classes('w-full')
            otp_field = ui.input(label='Enter OTP',placeholder='123456').classes('w-full').props('disabled')
            otp_button = ui.button('Login').classes('bg-black text-white font-bold').classes('w-full').props('disabled')
            ui.link('Use password instead').classes('text-black text-small')


ui.run() 