from nicegui import ui, app
from python_quant.utils.text import print_intro_message

@ui.page("/")
def index():
    for url in app.urls:
        ui.link(url, target=url)


def start_app(debug: bool = False) -> None:
    print_intro_message()
    ui.run(title="PyQuant Web App", port=8080, reload=False, show=False, dark=True)
