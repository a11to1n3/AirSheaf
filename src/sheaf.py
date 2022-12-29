from typing import Tuple, List, Dict, Callable, Union
import copy
import numpy as np
import datetime
import networkx as nx


class FaceBase:
    def __init__(self,
                name: str,
                value: Union[float,List[float]] = 0,
                d: int = 0,
                ) -> None:

        self.name = name
        self.value = value
        self.d = d

    def set_value(self, value: float) -> None:
        self.value = value

    def get_value(self) -> Union[float,List[float]]:
        return self.value

    def set_name(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_face_level(self, d: float) -> None:
        self.d = d

    def get_face_level(self) -> int:
        return self.d

    def get_direct_superfaces(self) -> List:
        return self._is_subface_of

    def set_superface(self, superface, restriction_map: Callable[[float], float]) -> None:
        self._is_subface_of.append(superface.get_name())
        self._restriction_to_superface[superface.get_name()] = restriction_map

    def lift_up_to_superface(self, superface) -> float:
        return self._restriction_to_superface[superface](self.value)

    def lift_up_to_superface_func(self, superface) -> Callable:
        return self._restriction_to_superface[superface]

class Vertex(FaceBase):
    def __init__(self,
                name: str,
                value: float = 0,
                ) -> None:

        super().__init__(name, value, 0)
        self._is_connected_to = []
        self._is_subface_of = []
        self._restriction_to_superface = {}

    def connect_to_vertex(self, vertex) -> None:
        self._is_connected_to.append(vertex)

    def get_connected_vertices(self) -> List:
        return self._is_connected_to

    def get_subfaces(self) -> List:
        return []

class Face(FaceBase):
    def __init__(self,
                name: str,
                value: List = [],
                d: int = 1,
                ) -> None:

        super().__init__(name, value, d)
        self._is_connected_to = []
        self._is_subface_of = []
        self._is_superface_of = []
        self._restriction_to_superface = {}
        self._consistency_threshold = 0
    
    def connect_to_face(self, face) -> None:
        self._is_connected_to.append(face)

    def get_connected_faces(self) -> List:
        return self._is_connected_to

    def set_subface(self, subface) -> None:
        self._is_superface_of.append(subface.get_name())

    def get_subfaces(self) -> List:
        return self._is_superface_of

    def set_consistency_threshold(self, thres) -> None:
        self._consistency_threshold = thres

    def get_consistency_threshold(self) -> float:
        return self._consistency_threshold

class Sheaf:
    def __init__(self) -> None:
        self.faces = {}
        self.consistency_filtration = {}
        self.values = []

    def _set_vertex(self, vertex: type[Vertex]) -> None:
        if "0-face" in list(self.faces.keys()):
            self.faces["0-face"][vertex.name] = vertex
        else:
            self.faces["0-face"] = {}
            self.faces["0-face"][vertex.name] = vertex
    
    def set_vertices(self, list_of_vertices:List[type[Vertex]]) -> None:
        [self._set_vertex(vertex) for vertex in list_of_vertices]

    def get_vertex(self, vertex_name: str):
        if vertex_name in self.faces["0-face"]:
            return self.faces["0-face"][vertex_name]
        
        raise ValueError

    def _set_face(self, face) -> None:
        if f"{face.d}-face" in list(self.faces.keys()):
            self.faces[f"{face.d}-face"][face.name] = face
        else:
            self.faces[f"{face.d}-face"] = {}
            self.faces[f"{face.d}-face"][face.name] = face

    def set_faces(self, list_of_faces:List[type[Face]]) -> None:
        [self._set_face(face) for face in list_of_faces]

    def get_face(self, face_name: str):
        for i in range(1, len(self.faces)):
            if face_name in self.faces[f"{i}-face"]:
                return self.faces[f"{i}-face"][face_name]

        raise ValueError

    def _check_faces_exist(self, faces: List[Union[type[Face],type[Vertex]]]) -> bool:
        if f"{faces[0].d}-face" not in list(self.faces.keys()) and not set(faces).issubset(list(self.faces.values())):
            return False

        return True

    def set_higher_faces(self,
                          list_of_superfaces: Dict[str, Union[Dict[str, Dict[str, Union[type[Face],type[Vertex]]]],Dict[str, Dict[str, Callable]]]]
                        ) -> None:

        for superface in list_of_superfaces:
            assert self._check_faces_exist(list(list_of_superfaces[superface]["subfaces"].values())), "One/All of the faces are not existed in Sheaf"
            combined_higher_face = Face(superface, d=list(list_of_superfaces[superface]["subfaces"].values())[0].d + 1)
            for subface in list_of_superfaces[superface]["subfaces"]:
                combined_higher_face.set_subface(list_of_superfaces[superface]["subfaces"][subface])
                list_of_superfaces[superface]["subfaces"][subface].set_superface(combined_higher_face, list_of_superfaces[superface]["restriction_map"][subface])
            self._set_face(combined_higher_face)

    def _update_vertices(self, value_of_vertices:Dict[str, Union[Tuple[float,float], Tuple[float,Tuple[float]]]]) -> None:
        for vertex in value_of_vertices:
            self.faces["0-face"][vertex].set_value(value_of_vertices[vertex][1:])

    @staticmethod
    def _calculate_value_spread(data_list: List[float]):
        if type(data_list[0]) == list and len(data_list[0]) == 1:
            return np.sqrt((np.cov([data[0] for data in data_list])))
        elif type(data_list[0]) == list:
            return np.sqrt(np.trace(np.cov(np.array(data_list).T)))

        return np.sqrt(np.sum(np.cov(data_list)))

    def _update_consistency_filtration(self, face, consistency_threshold):
        self.consistency_filtration[face] = consistency_threshold

    def _reset_consistency_filtration(self):
        self.consistency_filtration = {}

    def get_consistency_filtration(self) -> Dict[str, float]:
        return self.consistency_filtration

    def _propagate_level_by_level(self) -> None:
        self._reset_consistency_filtration()
        for d in self.faces:
            if d != "0-face":
                for face in self.faces[d]:
                    value_list = []
                    running_faces = [self.faces[d][face]]
                    subfaces = {}
                    subfaces[face] = []
                    paths = []
                    for i in range(self.faces[d][face].get_face_level()-1,-1,-1):
                        if len(running_faces) == 0:
                            break
                        
                        temp = []
                        while len(running_faces) != 0:
                            curr_face = running_faces.pop(0)
                            for f in self.faces[f"{i}-face"]:
                                if i > 0:
                                    fa = self.get_face(f)
                                else:
                                    fa = self.get_vertex(f)
                                if fa.get_face_level() != 0 and curr_face.name in fa.get_direct_superfaces():
                                    subfaces[curr_face.name].append(fa.name)
                                    temp.append(fa)
                                    subfaces[fa.name] = []
                                elif fa.get_face_level() == 0 and curr_face.name in fa.get_direct_superfaces():
                                    subfaces[curr_face.name].append(fa.name)
                                    back = [curr_face.name]
                                    path = fa.name+f"-{curr_face.name}"
                                    while len(back) != 0:
                                        curr = back.pop(0)
                                        for key, val in subfaces.items():
                                            if curr in val:
                                                back.append(key)
                                                path += f"-{key}"
                                    paths.append(path)

                        else:
                            running_faces = temp
                    
                    for path in paths:
                        nodes = path.split("-")
                        value = self.get_vertex(nodes[0]).value
                        for idx in range(len(nodes)-1):
                            if idx == 0:
                                subface = self.get_vertex(nodes[idx])
                            else:
                                subface = self.get_face(nodes[idx])

                            value = subface.lift_up_to_superface_func(nodes[idx+1])(value)
                        
                        if type(value) == list and len(value) == 1:
                            value_list.append(value[0])
                        else:
                            value_list.append(value)

                    self.faces[d][face].set_value(value_list)
                    consistency_threshold = self._calculate_value_spread(value_list)
                    self.faces[d][face].set_consistency_threshold(consistency_threshold)
                    self._update_consistency_filtration(face, consistency_threshold)

    def propagate(self, value_of_vertices:Dict[str, Union[float, Tuple[float]]]) -> None:
        self._update_vertices(value_of_vertices)
        self._propagate_level_by_level()
        self.consistency_filtration = {k: v for k, v in sorted(self.consistency_filtration.items(), key=lambda item: item[1])}
        self.consistency_radius = self.consistency_filtration[list(self.consistency_filtration.keys())[-1]]
        value_list = []
        for i in range(len(self.consistency_filtration)):
            if list(self.consistency_filtration.values())[i] <= np.mean(list(self.consistency_filtration.values())) + 0.5*np.std(list(self.consistency_filtration.values())):
                face = self.get_face(list(self.consistency_filtration.keys())[i])
                value_list.append(np.mean(face.value))

        self.value = np.mean(value_list)

    def visualize_sheaf_as_digraph(self) -> type[nx.MultiDiGraph()]:
        G = nx.MultiDiGraph()
        for d in range(len(self.faces)):
            for face in self.faces[f"{d}-face"]:
                G.add_node(face)
                subfaces = self.faces[f"{d}-face"][face].get_subfaces()
                if len(subfaces) > 0:
                    for subface in subfaces:
                        G.add_edge(subface, face)

        return G
