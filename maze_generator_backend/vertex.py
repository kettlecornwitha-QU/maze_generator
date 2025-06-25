from typing import Tuple, Set


class Vertex:
	def __init__(
		self, 
		*, 
		locus: Tuple[int], 
		is_open: bool, 
		free_end: bool, 
		last_visit: int, 
		connections: Set[str], 
		is_terminus: bool
	) -> None:
		self.locus = locus
		self.is_open = is_open
		self.free_end = free_end
		self.last_visit = last_visit
		self.connections = connections
		self.is_terminus = is_terminus

	def __str__(self):
		return (
			f'Vertex(Locus: {self.locus}, is_open: {self.is_open}, free_end: '
			f'{self.free_end}, connections: {self.connections})'
		)

	def kill_free_end(self) -> None:
		self.free_end = False
		self.last_visit = None