from typing import Optional, Callable, Dict
from nicegui import ui
import urllib.parse

# ---------------- NAV ROUTES ---------------- #
NAV_ROUTES = {
    'Campaigns': '/dashboard',
    'Areas': '/areas',
    'Campaign Schedules': '/schedules',
    'Search': '/search'
}

# ---------------- Sidebar Component ---------------- #
class Sidebar:
    def __init__(self, on_nav: Callable[[str], None], active_nav: str = 'Campaigns', logo_src: Optional[str] = None):
        self.on_nav = on_nav
        self.active_nav = active_nav
        self.logo_src = logo_src or self._default_logo_dataurl()
        self.buttons = {}
        self.root = None

    def _default_logo_dataurl(self) -> str:
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="32">'
            '<rect width="100%" height="100%" fill="#000000" rx="4" />'
            '<text x="10" y="22" font-family="Inter, Arial, sans-serif" font-size="14" fill="#FFFFFF">Novolab</text>'
            '</svg>'
        )
        return 'data:image/svg+xml;utf8,' + urllib.parse.quote(svg)

    def build(self):
        # idempotent build inside page functions
        if self.root is not None:
            return

        self.root = ui.column().classes(
            'bg-black text-white h-screen w-64 m-0 p-0 gap-0 fixed left-0 top-0 flex flex-col justify-between items-stretch'
        )

        with self.root:
            # Logo at very top-left (minimal padding)
            with ui.row().classes('items-center justify-start p-1'):
                ui.image(self.logo_src).classes('h-8 w-auto object-contain').style('display:block;')

            # Management heading immediately under the logo (no vertical gap)
            ui.label('Management').classes('font-semibold text-gray-400 text-sm pl-3').style('margin:0; padding:0;')

            # Compact navigation buttons, directly under the Management heading
            options = ['Campaigns', 'Areas', 'Campaign Schedules', 'Search']
            with ui.column().classes('gap-0 w-full').style('margin:0; padding:0;'):
                for opt in options:
                    # Use icon prop to show a small circle; we'll switch icon for active later
                    btn = ui.button(opt, on_click=lambda opt=opt: self.on_nav(opt))
                    btn.props(f'icon=radio_button_unchecked')  # small circle on left
                    btn.classes(
                        'block text-left text-sm px-3 py-2 w-full rounded-none '
                        'hover:bg-gray-800 transition-colors duration-150 flex items-center gap-2'
                    )
                    self.buttons[opt] = btn
                    self._set_active(btn, opt == self.active_nav)

        # Sign out at bottom (padded)
        with self.root:
            with ui.column().classes('w-full p-4'):
                signout_btn = ui.button('Sign out', on_click=self._sign_out)
                signout_btn.classes('w-full rounded-md px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold')

    def _set_active(self, btn, active: bool):
        # set full classes each time to avoid class accumulation
        if active:
            btn.props('icon=radio_button_checked')
            btn.classes(
                'block text-left text-sm px-3 py-2 w-full rounded-none '
                'bg-blue-600 hover:bg-blue-700 transition-colors duration-150 '
                'flex items-center gap-2 font-semibold text-white border-l-4 border-blue-800'
            )
        else:
            btn.props('icon=radio_button_unchecked')
            btn.classes(
                'block text-left text-sm px-3 py-2 w-full rounded-none '
                'bg-black hover:bg-gray-800 transition-colors duration-150 '
                'flex items-center gap-2 font-normal text-white border-l-0'
            )

    def update_active(self, active: str):
        self.active_nav = active
        if self.root is None:
            return
        for name, btn in self.buttons.items():
            self._set_active(btn, name == active)

    def _sign_out(self):
        ui.run_javascript("if (typeof navigate !== 'undefined' && navigate.to) { navigate.to('/'); } else { window.location.href = '/'; }")


# ---------------- CampaignCard (dashboard row) ---------------- #
class CampaignCard:
    def __init__(self,
                 campaign_id: str,
                 description: str,
                 cameras: int,
                 reports: int,
                 image_src: str = '',
                 video_src: Optional[str] = None,
                 disabled: bool = False):
        self.campaign_id = campaign_id
        self.description = description
        self.cameras = cameras
        self.reports = reports
        self.image_src = image_src
        self.video_src = video_src
        self.disabled = disabled
        self.root = None

    def build(self):
        wrapper_classes = (
            'rounded-lg shadow-sm bg-white overflow-hidden flex flex-col opacity-70'
            if self.disabled else
            'rounded-lg shadow-sm bg-white overflow-hidden transition-transform duration-200 hover:scale-105 hover:shadow-lg flex flex-col'
        )

        wrapper = ui.element('div').classes(wrapper_classes).style(
            'flex: 0 0 calc((100% - 2rem)/3); max-width: calc((100% - 2rem)/3); position: relative;'
        )

        with wrapper:
            with ui.element('div').classes('relative flex-[3] w-full bg-gray-200'):
                ui.image(self.image_src).classes('w-full h-full object-cover rounded-t-lg').style('display:block;')

                if not self.disabled and self.video_src:
                    def _play_internal():
                        with ui.dialog() as d:
                            try:
                                ui.video(self.video_src).classes('w-full')
                            except Exception:
                                ui.html(
                                    f'<video controls style="width:100%; height:auto;"><source src="{self.video_src}" type="video/mp4"></video>',
                                    sanitize=False
                                )
                        d.open()

                    ui.button('', on_click=_play_internal).props('icon=play_arrow').classes(
                        'absolute z-20 bg-white/95 hover:bg-white text-black p-2 rounded-full'
                    ).style('left: 50%; top: 50%; transform: translate(-50%, -50%); pointer-events: auto;')

            with ui.element('div').classes('flex-[2] bg-black text-white p-4 flex flex-col justify-between'):
                ui.label(self.description).classes('text-sm').style('margin: 0;')
                with ui.row().classes('items-center justify-between gap-2 mt-2'):
                    ui.label(f'{self.cameras} cameras').classes('text-sm text-white/90')
                    ui.label(f'{self.reports} insight reports').classes('text-sm text-white/90')
                if self.disabled:
                    ui.button('View campaign performance').classes(
                        'bg-gray-600 text-white rounded-md px-3 py-2 mt-3 opacity-60 cursor-not-allowed'
                    )
                else:
                    def _view_internal():
                        target = f"/campaign/{self.campaign_id}"
                        ui.run_javascript(
                            f"if (typeof navigate !== 'undefined' && navigate.to) {{ navigate.to({repr(target)}); }} else {{ window.location.href = {repr(target)}; }}"
                        )
                    ui.button('View campaign performance', on_click=_view_internal).classes(
                        'bg-green-600 hover:bg-green-700 text-white rounded-md px-3 py-2 mt-3'
                    )

            if self.disabled:
                with ui.element('div').classes('absolute inset-0 bg-black/40 z-30 flex items-center justify-center pointer-events-auto'):
                    ui.label('CLOSED').classes('text-white text-xl font-bold')

        self.root = wrapper
        return wrapper


# ---------------- PerformanceLeftCard (40%) ---------------- #
class PerformanceLeftCard:
    def __init__(self, image_src: str, date_text: str, cameras: int, reports: int, location_text: str):
        self.image_src = image_src
        self.date_text = date_text
        self.cameras = cameras
        self.reports = reports
        self.location_text = location_text

    def build(self):
        # left card uses flex-basis 40% so it is smaller than the video card
        card = ui.element('div').classes('rounded-lg shadow-sm bg-white overflow-hidden').style('flex: 0 0 40%; max-width: 40%;')
        with card:
            # fixed image height so both top cards match heights
            ui.image(self.image_src).classes('w-full h-64 object-cover rounded-t-lg').style('display:block;')
            with ui.element('div').classes('bg-black text-white p-4'):
                ui.label(self.date_text).classes('text-sm').style('margin:0;')
                ui.element('div').classes('h-px bg-white/30 my-2')
                with ui.row().classes('items-center justify-between'):
                    ui.label(f'{self.cameras} cameras').classes('text-sm text-white/90')
                    ui.label(f'{self.reports} report insights').classes('text-sm text-white/90')
                ui.label(self.location_text).classes('text-sm mt-3').style('color:#FFFFFF;')
        return card


# ---------------- CameraFeedCard (60%) ---------------- #
class CameraFeedCard:
    def __init__(self, initial_camera: int, camera_sources: Dict[int, Dict[str, str]]):
        self.camera = initial_camera
        self.camera_sources = camera_sources
        self.container = None

    def build(self):
        # right card uses flex-basis 60%
        self.container = ui.element('div').classes('rounded-lg shadow-sm bg-white overflow-hidden').style('flex: 0 0 60%; max-width: 60%;')
        self.render_media()
        return self.container

    def render_media(self):
        self.container.clear()
        src = self.camera_sources.get(self.camera, {})
        poster = src.get('poster', '')
        video = src.get('video', '')

        with self.container:
            # Render a single video element (use poster attribute if provided).
            # Use ui.video if available; otherwise fall back to ui.html with sanitize=False.
            video_html = f'<video controls playsinline style="width:100%; height:360px; object-fit:cover; border-radius:8px;"'
            if poster:
                video_html += f' poster="{poster}"'
            video_html += f'>'
            if video:
                video_html += f'<source src="{video}" type="video/mp4">'
            video_html += 'Your browser does not support the video element.</video>'

            try:
                # Prefer ui.video if present
                ui.video(video).classes('w-full').style('height:360px; object-fit:cover; border-radius:8px;')
            except Exception:
                # fallback to raw HTML (handle NiceGUI versions that accept sanitize)
                try:
                    ui.html(video_html, sanitize=False)
                except TypeError:
                    ui.html(video_html)

    def set_camera(self, camera_id: int):
        if camera_id not in self.camera_sources:
            return
        self.camera = camera_id
        self.render_media()


# ---------------- Helper: create & build sidebar per page ---------------- #
def make_sidebar_for_page(active_nav: str):
    def on_nav(nav_name: str):
        sidebar.update_active(nav_name)
        route = NAV_ROUTES.get(nav_name, '/dashboard')
        ui.run_javascript(
            f"if (typeof navigate !== 'undefined' && navigate.to) {{ navigate.to({repr(route)}); }} else {{ window.location.href = {repr(route)}; }}"
        )

    sidebar = Sidebar(on_nav=on_nav, active_nav=active_nav)
    sidebar.build()
    sidebar.update_active(active_nav)
    return sidebar


# ---------------- DASHBOARD PAGE ---------------- #
@ui.page('/dashboard')
def dashboard_page():
    sidebar = make_sidebar_for_page('Campaigns')

    container = ui.column().classes('ml-64 h-screen w-[calc(100%-16rem)] m-0 p-6 gap-6 bg-white overflow-auto')
    with container:
        ui.label('Dashboard').classes('text-4xl font-bold').style('margin:0;')
        ui.label('Your sightline insights for July 2025').classes('text-base text-gray-600 mt-1 mb-4')

        with ui.row().classes('w-full gap-4 items-start').style('flex-wrap: nowrap; align-items:flex-start;'):
            cars_image = 'https://images.pexels.com/photos/170811/pexels-photo-170811.jpeg'
            sample_video = 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4'

            c1 = CampaignCard(
                campaign_id='n1-western-bypass',
                description="The N1 Western Bypass between Rivonia Road and William Mooi Road",
                cameras=2,
                reports=27,
                image_src=cars_image,
                video_src=sample_video,
                disabled=False
            )
            c1.build()

            c2 = CampaignCard(
                campaign_id='m1-corridor',
                description="The M1 corridor around Johannesburg CBD",
                cameras=3,
                reports=30,
                image_src=cars_image,
                video_src=sample_video,
                disabled=True
            )
            c2.build()

            c3 = CampaignCard(
                campaign_id='r21-highway',
                description="The R21 highway near O.R. Tambo International Airport",
                cameras=4,
                reports=36,
                image_src=cars_image,
                video_src=sample_video,
                disabled=True
            )
            c3.build()


# ---------------- CAMPAIGN PERFORMANCE PAGE (final) ---------------- #
@ui.page('/campaign/{campaign_id}')
def campaign_performance_page(campaign_id: str):
    # build sidebar and set active
    sidebar = make_sidebar_for_page('Campaigns')

    page = ui.column().classes('ml-64 p-6 bg-white min-h-screen gap-6')

    # header row: back + title at left, camera toggles at right
    with page:
        with ui.row().classes('items-center justify-between w-full').style('gap:8px;'):
            with ui.row().classes('items-center gap-3'):
                ui.button('←', on_click=lambda: ui.run_javascript("navigate.to('/dashboard')")).classes(
                    'rounded-full bg-black text-white w-9 h-9 flex items-center justify-center'
                )
                ui.label(f'Campaign — {campaign_id}').classes('text-xl font-semibold')

            with ui.row().classes('items-center gap-2'):
                btn_cam1 = ui.button('Camera 1')
                btn_cam2 = ui.button('Camera 2')
                # black with white text as requested
                btn_cam1.classes('rounded-md px-3 py-1 bg-black text-white')
                btn_cam2.classes('rounded-md px-3 py-1 bg-black text-white')

    # top content row: left info 40% and right video 60% (top-aligned)
    with page:
        with ui.row().classes('w-full gap-4').style('align-items:flex-start;'):
            left_card = PerformanceLeftCard(
                image_src='https://images.pexels.com/photos/170811/pexels-photo-170811.jpeg',
                date_text='Your sightline insights for October 1, 2025',
                cameras=2,
                reports=27,
                location_text='The N1 western bypass between Rivonia Road and William Nicole Road'
            )
            left_card.build()

            camera_sources = {
                1: {
                    'video': 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4',
                    'poster': 'https://images.pexels.com/photos/170811/pexels-photo-170811.jpeg'
                },
                2: {
                    'video': 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4',
                    'poster': 'https://images.pexels.com/photos/340923/pexels-photo-340923.jpeg'
                }
            }
            camera_card = CameraFeedCard(initial_camera=1, camera_sources=camera_sources)
            camera_card.build()

    # black section under top row with chart (70%) + KPI column (30%)
    with page:
        with ui.element('div').classes('w-full rounded-lg').style('background:#0b0b0c; padding:16px;'):
            with ui.row().classes('w-full gap-4').style('align-items:flex-start;'):
                # chart left (70%)
                chart_card = ui.element('div').classes('rounded-lg bg-white p-4 shadow-sm').style('flex: 0 0 70%; max-width:70%;')
                with chart_card:
                    ui.label('Number of Cars Passing N1 Western Bypass').classes('text-sm font-semibold')
                    ui.html('''
                        <svg width="100%" height="180" viewBox="0 0 600 180" xmlns="http://www.w3.org/2000/svg">
                          <rect width="100%" height="100%" fill="#ffffff" rx="8"/>
                          <polyline fill="none" stroke="#2563EB" stroke-width="2" points="20,120 80,90 140,100 200,80 260,95 320,110 380,100 440,105 500,95"/>
                        </svg>
                    ''', sanitize=False)

                # KPI column (30%)
                with ui.column().classes('gap-4').style('flex: 0 0 30%; max-width:30%;'):
                    with ui.card().classes('p-4 rounded-lg shadow-sm'):
                        ui.label('235M').classes('text-2xl font-bold')
                        ui.label('PR Value Generated').classes('text-sm text-gray-600')
                    with ui.card().classes('p-4 rounded-lg shadow-sm'):
                        ui.label('Highest Difference').classes('text-sm font-semibold')
                        ui.label('MTN B Campaign').classes('text-sm text-gray-600')
                        ui.label('-7.1M').classes('text-xl font-bold text-red-600')
                    with ui.card().classes('p-4 rounded-lg shadow-sm'):
                        ui.label('Sales Volume Variance').classes('text-sm font-semibold')
                        ui.label('-11M (-10%)').classes('text-sm text-red-600')

    # camera toggle logic
    def select_camera(cam_id: int):
        camera_card.set_camera(cam_id)
        # show active marker on selected button (keep black bg, add blue ring)
        if cam_id == 1:
            btn_cam1.classes('rounded-md px-3 py-1 bg-black text-white ring-2 ring-blue-500')
            btn_cam2.classes('rounded-md px-3 py-1 bg-black text-white ring-0')
        else:
            btn_cam1.classes('rounded-md px-3 py-1 bg-black text-white ring-0')
            btn_cam2.classes('rounded-md px-3 py-1 bg-black text-white ring-2 ring-blue-500')

    btn_cam1.on('click', lambda e: select_camera(1))
    btn_cam2.on('click', lambda e: select_camera(2))

    select_camera(1)


# ---------------- Placeholder pages ---------------- #
@ui.page('/areas')
def areas_page():
    sidebar = make_sidebar_for_page('Areas')
    container = ui.column().classes('ml-64 h-screen w-[calc(100%-16rem)] m-0 p-6 gap-6 bg-white overflow-auto')
    with container:
        ui.label('Areas').classes('text-3xl font-bold')
        ui.label('Placeholder content for Areas.').classes('text-sm text-gray-600')


@ui.page('/schedules')
def schedules_page():
    sidebar = make_sidebar_for_page('Campaign Schedules')
    container = ui.column().classes('ml-64 h-screen w-[calc(100%-16rem)] m-0 p-6 gap-6 bg-white overflow-auto')
    with container:
        ui.label('Campaign Schedules').classes('text-3xl font-bold')
        ui.label('Placeholder content for Campaign Schedules.').classes('text-sm text-gray-600')


@ui.page('/search')
def search_page():
    sidebar = make_sidebar_for_page('Search')
    container = ui.column().classes('ml-64 h-screen w-[calc(100%-16rem)] m-0 p-6 gap-6 bg-white overflow-auto')
    with container:
        ui.label('Search').classes('text-3xl font-bold')
        ui.label('Placeholder search page.').classes('text-sm text-gray-600')


# ---------------- Root redirect ---------------- #
@ui.page('/')
def index_page():
    ui.run_javascript("navigate.to('/dashboard')")


# ---------------- Run ---------------- #
if __name__ == '__main__':
    ui.run(port=8001)

