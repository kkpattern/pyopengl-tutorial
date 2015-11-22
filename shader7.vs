#version 130


out vec3 color;


void main(){
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
	color = vec3(1.0, 1.0, 1.0);
}
