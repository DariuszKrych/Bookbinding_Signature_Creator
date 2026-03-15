from main import main
import dearpygui.dearpygui as dpg


def create_gui():
    dpg.create_context()
    with dpg.window(label="Welcome to the Signature Creator"):
        dpg.add_text("Ipsum llorem, this is some example text!")
        dpg.add_button(label="Start", callback=main)
    dpg.create_viewport(title="Bookbinding Signature Creator", width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

create_gui()