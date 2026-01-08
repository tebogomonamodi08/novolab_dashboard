from nicegui import ui
from authentication_controller import send_otp, user_otp
import pages.dashboard  

@ui.page('/')
def login_page():
    ui.add_head_html('''
        <style>
        html,body { margin:0; 
                    padding:0; 
                    height:100%; 
                     width:100%; 
                     background-color:black; }
        </style>
    ''')

    with ui.row().classes('bg-black w-screen h-screen justify-center items-center p-0 m-0'):
        with ui.card().classes('bg-white rounded-xl p-8'):
            with ui.column().classes('items-center space-y-3'):
                
                ui.label('Sign in with OTP').classes('font-bold text-xl m-0')
                ui.label('Enter email to get a one time password').classes('-mt-1')

                # Email input
                email_field = ui.input(label='Enter email', placeholder='tebogo@novo.com').classes('w-full')

                #Send OTP button
                async def handle_send_otp():
                    success = await asyncio.to_thread(send_otp, email_field.value)
                    if success:
                        ui.notify('OTP sent! Check your email', color='green')
                        otp_field.props(remove='disabled')
                        login_button.props(remove='disabled')
                    else:
                        ui.notify('Failed to send OTP', color='red')

                ui.button('Send OTP', on_click=asyncio.create_task(handle_send_otp()).classes('bg-black text-white font-bold').classes('w-full')

                # OTP input (disabled initially)
                otp_field = ui.input(label='Enter OTP', placeholder='123456').classes('w-full').props('disabled')

                # Login button (disabled initially)
                login_button = ui.button('Login').classes('bg-black text-white font-bold').props('disabled')

                # Login logic
                def handle_login():
                    if user_otp.get(email_field.value) == otp_field.value:
                        ui.navigate.to('/dashboard')  # Correct way to navigate
                    else:
                        ui.notify('Wrong OTP', color='red')

                login_button.on('click', handle_login)

ui.run(host='0.0.0.0',
      port=int(os.environ.get('PORT', 8000)),
    reload=False)
