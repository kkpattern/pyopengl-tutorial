#version 130


attribute vec3 position;
attribute vec3 normal;

uniform mat4 mvp;
uniform mat4 model;
uniform mat4 view;
uniform vec3 LightPosition_worldspace;

out vec3 color;
out vec3 Normal_cameraspace;
out vec3 LightDirection_cameraspace;
out float distance;


void main(){
	gl_Position = mvp*vec4(position, 1.0);
	vec3 vertexPosition_worldspace = (model*vec4(position, 1.0)).xyz;
	vec3 vertexPosition_cameraspace = (view*model*vec4(position, 1.0)).xyz;
	vec3 EyeDirection_cameraspace = vec3(0, 0, 0)-vertexPosition_cameraspace;

	vec3 LightPosition_cameraspace = (view*vec4(LightPosition_worldspace, 1)).xyz;
	LightDirection_cameraspace = LightPosition_cameraspace+EyeDirection_cameraspace;
	Normal_cameraspace = (view*model*vec4(normal, 0)).xyz;
	distance = length(vertexPosition_worldspace-LightPosition_worldspace);

	color = vec3(1.0, 1.0, 1.0);
}
