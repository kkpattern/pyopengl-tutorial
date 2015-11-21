import numpy

import OpenGL.GL as gl
import OpenGL.GLU as glu
from PyQt4 import QtOpenGL

import shader
import util


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

        vertices = numpy.array([
            [-1.0,-1.0,-1.0],
            [-1.0,-1.0, 1.0],
            [-1.0, 1.0, 1.0],
            [1.0, 1.0,-1.0],
            [-1.0,-1.0,-1.0],
            [-1.0, 1.0,-1.0],
            [1.0,-1.0, 1.0],
            [-1.0,-1.0,-1.0],
            [1.0,-1.0,-1.0],
            [1.0, 1.0,-1.0,],
            [1.0,-1.0,-1.0,],
            [-1.0,-1.0,-1.0],
            [-1.0,-1.0,-1.0],
            [-1.0, 1.0, 1.0],
            [-1.0, 1.0,-1.0],
            [1.0,-1.0, 1.0,],
            [-1.0,-1.0, 1.0],
            [-1.0,-1.0,-1.0],
            [-1.0, 1.0, 1.0],
            [-1.0,-1.0, 1.0],
            [1.0,-1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0,-1.0,-1.0],
            [1.0, 1.0,-1.0],
            [1.0,-1.0,-1.0],
            [1.0, 1.0, 1.0],
            [1.0,-1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0,-1.0],
            [-1.0, 1.0,-1.0],
            [1.0, 1.0, 1.0],
            [-1.0, 1.0,-1.0],
            [-1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0,],
            [-1.0, 1.0, 1.0,],
            [1.0,-1.0, 1.0],
        ], "f")
        self._vbo = gl.glGenBuffers (1)
        # ar = array("f", vertices)
        gl.glBindBuffer (gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glBufferData (gl.GL_ARRAY_BUFFER, vertices.size*4,
                        vertices, gl.GL_STATIC_DRAW)

        # Load texture.
        self._texture_data, self._width, self._height = util.load_bmp_custom("marble.bmp")
        self._uv_buffer_data = numpy.array([
             [0.000059, 1.0-0.000004],
             [0.000103, 1.0-0.336048],
             [0.335973, 1.0-0.335903],
             [1.000023, 1.0-0.000013],
             [0.667979, 1.0-0.335851],
             [0.999958, 1.0-0.336064],
             [0.667979, 1.0-0.335851],
             [0.336024, 1.0-0.671877],
             [0.667969, 1.0-0.671889],
             [1.000023, 1.0-0.000013],
             [0.668104, 1.0-0.000013],
             [0.667979, 1.0-0.335851],
             [0.000059, 1.0-0.000004],
             [0.335973, 1.0-0.335903],
             [0.336098, 1.0-0.000071],
             [0.667979, 1.0-0.335851],
             [0.335973, 1.0-0.335903],
             [0.336024, 1.0-0.671877],
             [1.000004, 1.0-0.671847],
             [0.999958, 1.0-0.336064],
             [0.667979, 1.0-0.335851],
             [0.668104, 1.0-0.000013],
             [0.335973, 1.0-0.335903],
             [0.667979, 1.0-0.335851],
             [0.335973, 1.0-0.335903],
             [0.668104, 1.0-0.000013],
             [0.336098, 1.0-0.000071],
             [0.000103, 1.0-0.336048],
             [0.000004, 1.0-0.671870],
             [0.336024, 1.0-0.671877],
             [0.000103, 1.0-0.336048],
             [0.336024, 1.0-0.671877],
             [0.335973, 1.0-0.335903],
             [0.667969, 1.0-0.671889],
             [1.000004, 1.0-0.671847],
             [0.667979, 1.0-0.335851]
        ], "f")
        self._uv_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._uv_buffer)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self._uv_buffer_data.size*4,
                        self._uv_buffer_data, gl.GL_STATIC_DRAW)
        self._shader_program = shader.LoadShaders("shader5.vs",
                                                  "shader5.ps")
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)

    def paintGL(self):
        gl.glClear (gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45.0, 4.0/3.0, 0.1, 100.0)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(4, 3, 3, 0, 0, 0, 0, 1, 0)

        self._texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture_id)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self._width, self._height, 0,
            gl.GL_BGR, gl.GL_UNSIGNED_BYTE, self._texture_data)
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
            gl.GL_LINEAR_MIPMAP_LINEAR)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)



        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
        gl.glEnableVertexAttribArray(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._uv_buffer)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glBindAttribLocation(self._shader_program, 1, "vertex_uv")
        gl.glLinkProgram(self._shader_program)
        gl.glUseProgram(self._shader_program)
        print gl.glGetProgramiv(self._shader_program, gl.GL_LINK_STATUS)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 12*3)
