#version 130

attribute vec3 InColor;
out vec3 outColor;


void main(){
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	outColor = InColor;
}
