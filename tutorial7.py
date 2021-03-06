import math

import OpenGL.GL as gl
import OpenGL.GLU as glu
from PyQt4 import QtOpenGL

import shader
import util
import math3d


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

        self._vertices, self._normals = util.load_obj("monkey.obj")
        self._vbo = gl.glGenBuffers (1)
        # ar = array("f", vertices)
        gl.glBindBuffer (gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glBufferData (gl.GL_ARRAY_BUFFER, self._vertices.size*4,
                        self._vertices, gl.GL_STATIC_DRAW)

        self._shader_program = shader.LoadShaders("shader7.vs",
                                                  "shader7.ps")
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)

    def paintGL(self):
        gl.glClear (gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45.0, 4.0/3.0, 0.1, 100.0)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(4, 3, 10, 0, 0, 0, 0, 1, 0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)

        gl.glLinkProgram(self._shader_program)
        gl.glUseProgram(self._shader_program)

        model = math3d.Matrix44.translate(0, 0, 0)

        view = math3d.Matrix44.look_at_right_hand(
            math3d.Vector(4, 3, 10),
            math3d.Vector(0, 0, 0),
            math3d.Vector(0, 1, 0))

        projection = math3d.Matrix44.projection_right_hand(
            math.radians(45), 4.0/3.0, 0.1, 100.0)

        mvp = model*view*projection

        mvp_id = gl.glGetUniformLocation(self._shader_program, "mvp")
        gl.glUniformMatrix4fv(mvp_id, 1, gl.GL_FALSE, mvp.raw_data())

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self._vertices.size)
