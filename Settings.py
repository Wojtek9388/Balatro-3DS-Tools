import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw

Window = {
    "Title": "3DS Balatro Tool",
    "Size": (800, 600),
    "Resizeable": glfw.FALSE,
}

ImguiFlags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_MOVE
