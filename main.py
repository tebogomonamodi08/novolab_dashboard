import asyncio
import os
from nicegui import ui
from authentication_controller import send_otp, user_otp
import pages.dashboard  

@ui.page('/')
def login_page():
    ui.add_head_html('''
        <style>
        html,body { margin:0; padding:0; height:100%; width:100%; background-color:black; }
        </style>
    ''')

    with ui.row().classes('bg-black w-screen h-screen justify-center items-center p-0 m-0'):
        with ui.card().classes('bg-white rounded-xl p-8 w-[420px]'):
            with ui.column().classes('items-center space-y-3'):
                
                ui.label('Sign in with OTP').classes('font-bold text-xl m-0')
                ui.label('Enter email to get a one time password').classes('-mt-1')

                # Email input
                email_field = ui.input(label='Enter email', placeholder='tebogo@novo.com').classes('w-full')

                # OTP input (disabled initially) — set disabled via props, not via keyword
                otp_field = ui.input(label='Enter OTP', placeholder='123456').classes('w-full').props('disabled')

                # Login button (disabled initially)
                login_button = ui.button('Login').classes('bg-black text-white font-bold').props('disabled')

                # Send OTP button
                send_button = ui.button(
                    'Send OTP',
                ).classes('bg-black text-white font-bold w-full')

                async def handle_send_otp():
                    if not email_field.value or not email_field.value.strip():
                        ui.notify('Please enter an email', color='red')
                        return

                    # show loading state on the send button
                    send_button.props('loading')
                    try:
                        success = await asyncio.to_thread(send_otp, email_field.value.strip())
                        if success:
                            ui.notify('OTP sent! Check your email', color='green')
                            otp_field.props(remove='disabled')
                            login_button.props(remove='disabled')

                            # optional debug: reveal OTP when DEV_SHOW_OTP is enabled
                            if os.getenv('DEV_SHOW_OTP', 'false').lower() in ('1', 'true', 'yes'):
                                otp = user_otp.get(email_field.value.strip())
                                ui.notify(f'DEBUG OTP: {otp}', color='blue', timeout=5000)
                                print(f'DEBUG OTP for {email_field.value.strip()}: {otp}')
                        else:
                            ui.notify('Failed to send OTP. Check logs / env vars', color='red')
                    finally:
                        send_button.props(remove='loading')

                # schedule the async handler when the button is clicked
                send_button.on('click', lambda: asyncio.create_task(handle_send_otp()))

                # Login logic
                def handle_login():
                    if user_otp.get(email_field.value.strip()) == otp_field.value:
                        ui.notify('Login successful', color='green')
                        ui.open('/dashboard')
                    else:
                        ui.notify('Wrong OTP', color='red')

                login_button.on('click', handle_login)

# Correct port binding for Render
ui.run(
    host='0.0.0.0',
    port=int(os.environ.get('PORT', 8000)),
    reload=False
)
