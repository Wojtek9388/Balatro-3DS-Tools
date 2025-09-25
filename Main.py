# Menu Stuffs
import imgui
from imgui.integrations.glfw import GlfwRenderer

# Opengl Stuff
import glfw
from OpenGL.GL import *

# Misc
import sys

from Settings import *

from DeckStuffs import *
from AudioStuffs import *

if sys.version_info.major != 3 and sys.version_info.minor != 11:
    sys.exit("Outdated")

def main():
    if not glfw.init():
        print("Could not initialize GLFW")
        return

    glfw.window_hint(glfw.RESIZABLE, Window["Resizeable"])
    window = glfw.create_window(Window["Size"][0], Window["Size"][1], Window["Title"], None, None)
    glfw.make_context_current(window)

    imgui.create_context()
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        imgui.new_frame()

        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(Window["Size"][0], Window["Size"][1], condition=imgui.ALWAYS)

        imgui.begin(Window["Title"], flags=ImguiFlags)

        # Audio Tools
        AudioGui()

        DeckCreationGui()
        DeckEditorGui()

        imgui.end()

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()
