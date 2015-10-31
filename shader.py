import OpenGL.GL as gl


def LoadShaders(vertex_file_path, fragment_file_path):
    vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    with open(vertex_file_path, "r") as f:
        vertex_shader_code = f.read()
    with open(fragment_file_path, "r") as f:
        fragment_shader_code = f.read()

    gl.glShaderSource(vertex_shader, vertex_shader_code)
    gl.glCompileShader(vertex_shader)
    result = gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS)
    info_log = gl.glGetShaderInfoLog(vertex_shader)
    print result, info_log

    gl.glShaderSource(fragment_shader, fragment_shader_code)
    gl.glCompileShader(fragment_shader)
    result = gl.glGetShaderiv(fragment_shader, gl.GL_COMPILE_STATUS)
    info_log = gl.glGetShaderInfoLog(fragment_shader)
    print result, info_log

    program = gl.glCreateProgram()
    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)
    gl.glLinkProgram(program)
    result = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    info_log = gl.glGetProgramInfoLog(program)
    print result, info_log

    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)
    return program
