import struct

import numpy


HEADER_SIZE = 54


def load_bmp_custom(image_path):
	with open(image_path, "rb") as f:
		header = f.read(HEADER_SIZE)
		if len(header) == HEADER_SIZE:
			if header[0] == "B" and header[1] == "M":
				data_pos = struct.unpack("i", header[0x0A:0x0A+4])[0]
				size = struct.unpack("i", header[0x22:0x22+4])[0]
				width = struct.unpack("i", header[0x12:0x12+4])[0]
				height = struct.unpack("i", header[0x16:0x16+4])[0]
				if data_pos == 0:
					data_pos = 54
				if size == 0:
					size = width*height*3
				f.read(data_pos-HEADER_SIZE)  # skip meta informations.
				result = f.read(size), width, height
			else:
				result = None, 0, 0
		else:
			result = None, 0, 0
	return result


def load_obj(obj_path):
    temp_vertex = []
    # temp_uv = []
    temp_normal = []
    temp_vertex_indices = []
    # temp_uv_indices = []
    temp_normal_indices = []
    flat_vertex = []
    flat_normal = []
    with open(obj_path, "r") as f:
        for line in f:
            header, data = line.split(" ", 1)
            if header == "v":
                temp_vertex.append([float(i) for i in data.split()])
            # elif header == "vt":
            #     temp_uv.append([float(i) for i in data.split()])
            elif header == "vn":
                temp_normal.append([float(i) for i in data.split()])
            elif header == "f":
                for vertex in data.split():
                    indices = [int(i) if i else -1 for i in vertex.split("/")]
                    temp_vertex_indices.append(indices[0])
                    # temp_uv_indices.append(indices[1])
                    temp_normal_indices.append(indices[2])
        for i in temp_vertex_indices:
            flat_vertex.append(temp_vertex[i-1])
        for i in temp_normal_indices:
            flat_normal.append(temp_normal[i-1])
    return numpy.array(flat_vertex, "f"), numpy.array(flat_normal, "f")


def load_obj_with_index(obj_path):
    temp_vertex = []
    # temp_uv = []
    temp_normal = []
    # temp_uv_indices = []
    vertex_map = {}
    next_index = 0
    vertex_buffer = []
    normal_buffer = []
    index_buffer = []
    with open(obj_path, "r") as f:
        for line in f:
            header, data = line.split(" ", 1)
            if header == "v":
                temp_vertex.append(tuple(float(i) for i in data.split()))
            # elif header == "vt":
            #     temp_uv.append([float(i) for i in data.split()])
            elif header == "vn":
                temp_normal.append(tuple(float(i) for i in data.split()))
            elif header == "f":
                for vertex in data.split():
                    indices = [int(i) if i else -1 for i in vertex.split("/")]
                    position = temp_vertex[indices[0]-1]
                    normal = temp_normal[indices[2]-1]
                    try:
                        index = vertex_map[(position, normal)]
                    except KeyError:
                        index = next_index
                        vertex_map[(position, normal)] = index
                        next_index += 1
                    index_buffer.append(index)
                    # temp_uv_indices.append(indices[1])
        for position, normal in sorted(vertex_map, key=lambda k: vertex_map[k]):
            vertex_buffer.append(position)
            normal_buffer.append(normal)
    return (
        numpy.array(vertex_buffer, "f"),
        numpy.array(normal_buffer, "f"),
        index_buffer)


def main():
    vertex, normal, index = load_obj_with_index("monkey.obj")
    print index.size


if __name__ == "__main__":
	main()
