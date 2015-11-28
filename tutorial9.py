import ctypes
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

        self._vertices, self._normals, self._indices = \
            util.load_obj_with_index("monkey.obj")
        a, b = util.load_obj("monkey.obj")
        self._vbo = gl.glGenBuffers(1)
        gl.glBindBuffer (gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glBufferData (gl.GL_ARRAY_BUFFER, self._vertices.size*4,
                        self._vertices, gl.GL_STATIC_DRAW)

        self._normal_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer (gl.GL_ARRAY_BUFFER, self._normal_vbo)
        gl.glBufferData (gl.GL_ARRAY_BUFFER, self._normals.size*4,
                        self._normals, gl.GL_STATIC_DRAW)

        self._index_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_buffer)
        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            len(self._indices)*4,
            (ctypes.c_uint*len(self._indices))(*self._indices),
            gl.GL_STATIC_DRAW)

        self._shader_program = shader.LoadShaders("shader9.vs",
                                                  "shader9.ps")
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LESS)

    def paintGL(self):
        gl.glClear (gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        gl.glLinkProgram(self._shader_program)
        gl.glUseProgram(self._shader_program)

        position_location = gl.glGetAttribLocation(self._shader_program,
                                                   "position")
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glEnableVertexAttribArray(position_location)
        gl.glVertexAttribPointer(position_location, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        normal_location = gl.glGetAttribLocation(self._shader_program, "normal")
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._normal_vbo)
        gl.glEnableVertexAttribArray(normal_location)
        gl.glVertexAttribPointer(normal_location, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        model = math3d.Matrix44.translate(0, 0, 0)

        view = math3d.Matrix44.look_at_right_hand(
            math3d.Vector(4, 3, 10),
            math3d.Vector(0, 0, 0),
            math3d.Vector(0, 1, 0))

        projection = math3d.Matrix44.projection_right_hand(
            math.radians(45), 4.0/3.0, 0.1, 100.0)

        mvp = model*view*projection

        model_id = gl.glGetUniformLocation(self._shader_program, "model")
        gl.glUniformMatrix4fv(model_id, 1, gl.GL_FALSE, model.raw_data())
        view_id = gl.glGetUniformLocation(self._shader_program, "view")
        gl.glUniformMatrix4fv(view_id, 1, gl.GL_FALSE, view.raw_data())

        mvp_id = gl.glGetUniformLocation(self._shader_program, "mvp")
        gl.glUniformMatrix4fv(mvp_id, 1, gl.GL_FALSE, mvp.raw_data())

        light_position = math3d.Vector(10, 10, 10);
        light_position_id = gl.glGetUniformLocation(
            self._shader_program, "LightPosition_worldspace")
        gl.glUniform3fv(light_position_id, 1, light_position.raw_data())


        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_buffer)
        gl.glDrawElements(gl.GL_TRIANGLES, len(self._indices),
                          gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        # gl.glDrawArrays(gl.GL_TRIANGLES, 0, self._vertices.size)
