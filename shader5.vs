#version 130

attribute vec2 vertex_uv;

out vec2 uv;


void main(){
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	uv = vertex_uv;
}
