import numpy

import OpenGL.GL as gl
import OpenGL.GLU as glu
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
        self._color_buffer_data = numpy.array([
                [0.583,  0.771,  0.014],
                [0.609,  0.115,  0.436],
                [0.327,  0.483,  0.844],
                [0.822,  0.569,  0.201],
                [0.435,  0.602,  0.223],
                [0.310,  0.747,  0.185],
                [0.597,  0.770,  0.761],
                [0.559,  0.436,  0.730],
                [0.359,  0.583,  0.152],
                [0.483,  0.596,  0.789],
                [0.559,  0.861,  0.639],
                [0.195,  0.548,  0.859],
                [0.014,  0.184,  0.576],
                [0.771,  0.328,  0.970],
                [0.406,  0.615,  0.116],
                [0.676,  0.977,  0.133],
                [0.971,  0.572,  0.833],
                [0.140,  0.616,  0.489],
                [0.997,  0.513,  0.064],
                [0.945,  0.719,  0.592],
                [0.543,  0.021,  0.978],
                [0.279,  0.317,  0.505],
                [0.167,  0.620,  0.077],
                [0.347,  0.857,  0.137],
                [0.055,  0.953,  0.042],
                [0.714,  0.505,  0.345],
                [0.783,  0.290,  0.734],
                [0.722,  0.645,  0.174],
                [0.302,  0.455,  0.848],
                [0.225,  0.587,  0.040],
                [0.517,  0.713,  0.338],
                [0.053,  0.959,  0.120],
                [0.393,  0.621,  0.362],
                [0.673,  0.211,  0.457],
                [0.820,  0.883,  0.371],
                [0.982,  0.099,  0.879],
        ], "f")
        self._color_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._color_buffer)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self._color_buffer_data.size*4,
                        self._color_buffer_data, gl.GL_STATIC_DRAW)
        self._shader_program = shader.LoadShaders("simple_es_shader.vs",
                                                  "simple_es_shader.ps")
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

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
        gl.glEnableVertexAttribArray(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._color_buffer)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glBindAttribLocation(self._shader_program, 1, "InColor")
        gl.glLinkProgram(self._shader_program)
        gl.glUseProgram(self._shader_program)
        print gl.glGetProgramiv(self._shader_program, gl.GL_LINK_STATUS)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 12*3)
