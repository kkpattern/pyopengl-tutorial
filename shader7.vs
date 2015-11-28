#version 130


uniform mat4 mvp;
out vec3 color;


void main(){
	gl_Position = mvp*gl_Vertex;
	color = vec3(1.0, 1.0, 1.0);
}
