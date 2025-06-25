#______________________________________________________________________________
from vertex import Vertex
from typing import Dict, Tuple, List
import random


class Build:
	def __init__(
		self, 
		height: int, 
		width: int, 
		branch_weight: float, 
		triple_weight: float, 
		verbose=False
	) -> None:
		self.height = height
		self.width = width
		self.branch_weight = branch_weight
		self.triple_weight = triple_weight
		self.verbose = verbose
		self.vertices = self.generate_starting_array()

	def generate_starting_array(self) -> Dict[Tuple, Vertex]:
		vertices = {}
		for i in range(self.height):
			for j in range(self.width):
				vertices.update({
					(i, j): Vertex(
						locus = (i, j), 
						is_open = True, 
						free_end = None, 
						last_visit = None, 
						connections = set(), 
						is_terminus = False
					)
				})
				if i == self.height - 1 and j == 0:
					vertices[(i, j)].is_open = False
					vertices[(i, j)].free_end = False
					vertices[(i, j)].connections.add('R')
					vertices[(i, j)].is_terminus = True
				if i == self.height - 1 and j == 1:
					vertices[(i, j)].is_open = False
					vertices[(i, j)].free_end = True
					vertices[(i, j)].last_visit = 0
					vertices[(i, j)].connections.add('L')
				if i == 0 and j == self.width - 1:
					vertices[(i, j)].is_open = False
					vertices[(i, j)].free_end = False
					vertices[(i, j)].connections.add('L')
					vertices[(i, j)].is_terminus = True
				if i == 0 and j == self.width - 2:
					vertices[(i, j)].free_end = False
					vertices[(i, j)].connections.add('R')
		return vertices

	def connect(self, src_v: Vertex, target_v: Vertex) -> None:
		direction_map = {
			(1, 0):  ('D', 'U'),
			(-1, 0): ('U', 'D'),
			(0, 1):  ('L', 'R'),
			(0, -1): ('R', 'L'),
		}
		row_dif = target_v.locus[0] - src_v.locus[0]
		col_dif = target_v.locus[1] - src_v.locus[1]
		delta = (row_dif, col_dif)
		if delta in direction_map:
			target_dir, src_dir = direction_map[delta]
			target_v.connections.add(target_dir)
			src_v.connections.add(src_dir)

	def grow_branch(self, src_v: Vertex, target_v: Vertex) -> None:
		if self.verbose:
			print(f'Connecting {src_v} to {target_v}')
		self.connect(src_v, target_v)
		src_v.free_end = False
		src_v.last_visit = None
		target_v.is_open = False
		if (self.get_possible_targets(target_v) and 
				target_v.locus != (0, self.width - 2)):
			target_v.free_end = True
			target_v.last_visit = 0

	def there_are_free_ends(self) -> bool:
		for v in self.vertices.values():
			if v.free_end is True:
				return True
		return False

	def choose_free_vertex(self) -> Vertex:
		free_vertices = [v for v in self.vertices.values() if v.free_end]
		return random.choice(free_vertices)

	def there_are_open_vertices(self) -> bool:
		for v in self.vertices.values():
			if v.is_open is True:
				return True
		return False

	def choose_open_vertex(self) -> Vertex:
		open_vertices = [v for v in self.vertices.values() if v.is_open]
		return random.choice(open_vertices)

	def inc_last_visit(self) -> None:
		for v in self.vertices.values():
			if v.last_visit is not None:
				v.last_visit += 1

	def should_branch(self) -> bool:
		return random.random() < self.branch_weight

	def should_triple_branch(self) -> bool:
		return random.random() < self.triple_weight

	def get_neighbors(self, src_v: Vertex) -> List[Vertex]:
		neighbors = []
		i, j = src_v.locus
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		for di, dj in directions:
			ni, nj = i + di, j + dj
			if 0 <= ni < self.height and 0 <= nj < self.width:
				neighbors.append(self.vertices[(ni, nj)])
		return neighbors
	
	def get_possible_targets(self, src_v: Vertex) -> List[Vertex]:
		targets = []
		for neighbor in self.get_neighbors(src_v):
			if not src_v.is_open:
				if neighbor.is_open:
					targets.append(neighbor)
			else:
				if not neighbor.is_open and not neighbor.is_terminus:
					targets.append(neighbor)
		return targets

	def targeting_all(self, targs: int, branch: bool, triple: bool) -> bool:
		return (
			targs == 1 or
			(targs == 2 and branch) or
			(targs == 3 and branch and triple)
		)

	def grow_free_ends_loop(self) -> None:
		while self.there_are_free_ends():
			src_v = self.choose_free_vertex()
			possible_targets = self.get_possible_targets(src_v)
			if not possible_targets:
				src_v.kill_free_end()
				continue
			targs = len(possible_targets)
			branch = self.should_branch()
			triple = self.should_triple_branch()
			if self.targeting_all(targs, branch, triple):
				for target in possible_targets:
					self.grow_branch(src_v, target)
				self.inc_last_visit()
				continue
			odd_man = random.choice(possible_targets)
			if not branch:
				self.grow_branch(src_v, odd_man)
				self.inc_last_visit()
				continue
			possible_targets.remove(odd_man)
			for target in possible_targets:
				self.grow_branch(src_v, target)
			self.inc_last_visit()
			continue

	def grow_tree(self) -> None:
		self.grow_free_ends_loop()
		if self.verbose:
			print('Ran out of free ends')
		while self.there_are_open_vertices():
			target_v = self.choose_open_vertex()
			possible_srcs = self.get_possible_targets(target_v)
			if not possible_srcs:
				continue
			chosen_src = random.choice(possible_srcs)
			self.grow_branch(chosen_src, target_v)
			self.grow_free_ends_loop()
			if self.verbose:
				print('Ran out of free ends')
			continue

	def export_maze_cells(self) -> List[Dict]:
		cells = []
		for vertex in self.vertices.values():
			i, j = vertex.locus
			is_start = (i == self.height - 1) and (j == 0)
			is_end = (i == 0) and (j == self.width - 1)
			walls = set('UDRL') - vertex.connections
			if is_start:
				walls.discard('L')
			if is_end:
				walls.discard('R')
			cells.append({
				'row': i, 
				'col': j, 
				'walls': sorted(walls)
			})
		return cells

	@classmethod
	def demo(cls) -> None:
		maze = cls(10, 10, 0.25, 0.25, verbose=True)
		maze.grow_tree()
		for vertex in maze.vertices.values():
			print(vertex)


if __name__ == '__main__':
	Build.demo()
