from array import array
import sys

import OpenGL.GL as gl
# import OpenGL.GLU as glu
from PyQt4 import QtGui
from PyQt4 import QtOpenGL

import shader


class Canvas(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.setFixedSize(800, 600)

    def initializeGL(self):
        gl.glClearColor(1.0,1.0,1.0,0.0)
        # gl.glColor3f(0.0,0.0, 0.0)
        # gl.glPointSize(4.0)
        # gl.glMatrixMode(gl.GL_PROJECTION)
        # gl.glLoadIdentity()
        # glu.gluOrtho2D(0.0,640.0,0.0,480.0)
        gl.glViewport (0, 0, 800, 600)
        gl.glClearColor (0.0, 0.5, 0.5, 1.0)
        gl.glEnableClientState (gl.GL_VERTEX_ARRAY)

        vertices = [ 0.0, 1.0, 0.0,  0.0, 0.0, 0.0,  1.0, 1.0, 0.0 ]
        self._vbo = gl.glGenBuffers (1)
        ar = array("f", vertices)
        gl.glBindBuffer (gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glBufferData (gl.GL_ARRAY_BUFFER, len(vertices)*4,
                      ar.tostring(), gl.GL_STATIC_DRAW)
        self._shader_program = shader.LoadShaders("simple_es_shader.vs",
                                                  "simple_es_shader.ps")

    def paintGL(self):
        gl.glClear (gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        gl.glUseProgram(self._shader_program)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        canvas = Canvas()
        self.setCentralWidget(canvas)


def main():
    app = QtGui.QApplication(["OpenGL Tutorial"])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
