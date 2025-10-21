from nicegui import ui

# ---------------- Sidebar Component ---------------- #
class Sidebar:
    def __init__(self, on_nav):
        self.on_nav = on_nav
        self.current_selection = "Campaigns"  # Default selection
        self.buttons = {}  # Store button references to update their state
        self._build()

    def _build(self):
        with ui.column().classes('bg-black text-white h-full w-64 p-0 justify-between'):  # No padding on main container
            # Top content - no gaps
            with ui.column().classes('w-full'):  # Remove all spacing
                # Header with padding
                ui.label('NOVOLAB').classes('text-lg font-bold p-3')  # Padding only on header
                
                # Management Section - no gaps
                with ui.column().classes('w-full'):
                    ui.label('MANAGEMENT').classes('font-bold text-gray-400 text-xs uppercase tracking-wider px-3 py-1')  # Padding only on label
                    self._add_nav_button('Campaigns')
                    self._add_nav_button('Areas')
                    self._add_nav_button('Campaign Schedules')
                    self._add_nav_button('Search')
                
                # Account and Settings Section - no gaps  
                with ui.column().classes('w-full'):
                    ui.label('ACCOUNT AND SETTINGS').classes('font-bold text-gray-400 text-xs uppercase tracking-wider px-3 py-1')
                    self._add_nav_button('Notifications')
                    self._add_nav_button('Email Address')
                
                # Billing and Subscriptions Section - no gaps
                with ui.column().classes('w-full'):
                    ui.label('BILLING AND SUBSCRIPTIONS').classes('font-bold text-gray-400 text-xs uppercase tracking-wider px-3 py-1')
                    self._add_nav_button('Billing History')
                    self._add_nav_button('Subscription Plan')
                    self._add_nav_button('Payment Methods')
            
            # Bottom section with Sign Out button - full width
            with ui.column().classes('w-full border-t border-gray-700'):
                ui.button(
                    'Sign Out',
                    on_click=lambda: ui.notify('Signing out...'),
                    icon='logout'
                ).props('flat color=white')\
                 .classes('w-full justify-start p-3 h-10 min-h-0 bg-red-600 hover:bg-red-700 transition-colors rounded-none')\
                 .style('text-transform: none; font-weight: normal;')

    def _add_nav_button(self, name):
        """Add a compact navigation button with full width"""
        is_active = (name == self.current_selection)
        bg_color = 'bg-blue-600' if is_active else 'bg-transparent hover:bg-gray-800'
        
        button = ui.button(
            name,
            on_click=lambda n=name: self._handle_selection(n)
        ).props('flat color=white dense')\
         .classes(f'w-full justify-start p-3 h-8 min-h-0 text-sm rounded-none {bg_color} transition-colors')\
         .style('text-transform: none; font-weight: normal; margin: 0;')
        
        self.buttons[name] = button

    def _handle_selection(self, selection):
        self.current_selection = selection
        self.on_nav(selection)
        # Update button styles without rebuilding
        self._update_button_styles()

    def _update_button_styles(self):
        """Update all button styles based on current selection"""
        for name, button in self.buttons.items():
            is_active = (name == self.current_selection)
            bg_color = 'bg-blue-600' if is_active else 'bg-transparent hover:bg-gray-800'
            # Remove existing background classes and add new ones
            button._classes = [cls for cls in button._classes if not cls.startswith('bg-')]
            button.classes(f'w-full justify-start p-3 h-8 min-h-0 text-sm rounded-none {bg_color} transition-colors')


# ---------------- Main Content Component ---------------- #
class MainContent:
    def __init__(self):
        self.container = ui.column().classes('p-6 h-full overflow-y-auto')

    def update(self, selection: str):
        self.container.clear()
        with self.container:
            ui.label(f'You selected: {selection}').classes('text-2xl font-bold mb-4')
            
            with ui.card().classes('w-full p-4'):
                ui.label(f'Content for {selection}').classes('text-lg font-semibold')
                
                if selection == "Campaigns":
                    ui.label('Manage your marketing campaigns here.').classes('text-gray-600')
                    with ui.column().classes('mt-4 space-y-2'):
                        ui.button('Create New Campaign', icon='add')
                        ui.button('View Existing Campaigns', icon='list')
                elif selection == "Areas":
                    ui.label('Configure different geographical areas.').classes('text-gray-600')
                elif selection == "Campaign Schedules":
                    ui.label('Schedule and manage campaign timelines.').classes('text-gray-600')
                elif selection == "Search":
                    ui.label('Search through your campaigns and content.').classes('text-gray-600')
                    ui.input(placeholder='Enter search term...').classes('w-full mt-2')
                elif selection == "Notifications":
                    ui.label('Configure your notification preferences.').classes('text-gray-600')
                    with ui.column().classes('mt-2'):
                        ui.checkbox('Email Notifications').classes('text-gray-700')
                        ui.checkbox('Push Notifications').classes('text-gray-700')
                elif selection == "Email Address":
                    ui.label('Manage your email settings and addresses.').classes('text-gray-600')
                    ui.input(placeholder='Your email address').classes('w-full mt-2')
                elif selection == "Billing History":
                    ui.label('View your billing history and invoices.').classes('text-gray-600')
                elif selection == "Subscription Plan":
                    ui.label('Manage your subscription plan.').classes('text-gray-600')
                elif selection == "Payment Methods":
                    ui.label('Update your payment methods.').classes('text-gray-600')
                else:
                    ui.label('This section is under development.').classes('text-gray-600')


# ---------------- Dashboard Layout ---------------- #
@ui.page('/dashboard')
def dashboard_page():
    ui.add_head_html('''
        <style>
            html, body, #app {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow: hidden;
            }
        </style>
    ''')

    def handle_nav(selection):
        main.update(selection)

    with ui.column().classes('w-full h-screen m-0 p-0 overflow-hidden'):
        with ui.row().classes('w-full h-full m-0 p-0 flex-nowrap'):
            # Single sidebar instance
            with ui.column().classes('w-64 h-full bg-black m-0 p-0'):
                sidebar = Sidebar(on_nav=handle_nav)
            
            # Main content
            with ui.column().classes('flex-1 h-full m-0 p-0 bg-gray-100'):
                main = MainContent()
    
    # Initialize with default selection
    main.update(sidebar.current_selection)

ui.run()



