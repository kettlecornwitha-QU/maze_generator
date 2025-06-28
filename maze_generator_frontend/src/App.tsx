import { useState } from "react";
import axios from "axios";
import "./App.css";

interface MazeCell {
	row: number;
	col: number;
	walls: string[]; // e.g. ['U', 'R', 'D']
}

const cellSize = 20; // in pixels

export default function App() {
	const [maze, setMaze] = useState<MazeCell[]>([]);
	const [rows, setRows] = useState(10);
	const [cols, setCols] = useState(10);
	const [rowsInput, setRowsInput] = useState("10");
	const [colsInput, setColsInput] = useState("10");
	const [branchWeight, setBranchWeight] = useState(0.25);
	const [tripleWeight, setTripleWeight] = useState(0.25);

	const fetchMaze = async () => {
		const h = parseInt(rowsInput);
		const w = parseInt(colsInput);

		try {
			const res = await axios.get("https://maze-backend-lj42.onrender.com/generate-maze", {
				params: {
					h,
					w,
					branch: branchWeight,
					triple: tripleWeight,
				},
			});
			setMaze(res.data.maze);
			setCols(w);
			setRows(h);
		} catch (err) {
			console.error("Error fetching maze:", err);
		}
	};

	return (
		<div className="app">
			<h1>Maze Generator</h1>

			<div className="controls">
				<label>
					Rows:
					<input
						type="number"
						min={1}
						value={rowsInput}
						onChange={(e) => setRowsInput(e.target.value)}
						onBlur={() => {
							const val = parseInt(rowsInput);
							if (!isNaN(val) && val > 0) setRows(val);
							else setRowsInput(rows.toString());
						}}
					/>
				</label>
				<label>
					Columns:
					<input
						type="number"
						min={1}
						value={colsInput}
						onChange={(e) => setColsInput(e.target.value)}
						onBlur={() => {
							const val = parseInt(colsInput);
							if (isNaN(val) || val <= 0) {
								setColsInput(cols.toString());
							}
						}}
					/>
				</label>
				<label>
					Branch Weight: {branchWeight.toFixed(2)}
					<input
						type="range"
						min={0}
						max={1}
						step={0.01}
						value={branchWeight}
						onChange={(e) => setBranchWeight(parseFloat(e.target.value))}
					/>
				</label>
				<label>
					3-Way Branch Weight: {tripleWeight.toFixed(2)}
					<input
						type="range"
						min={0}
						max={1}
						step={0.01}
						value={tripleWeight}
						onChange={(e) => setTripleWeight(parseFloat(e.target.value))}
					/>
				</label>
			</div>

			<button onClick={fetchMaze}>Generate New Maze</button>

			<div
				className="maze"
				style={{
					width: cols * cellSize,
					gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`
				}}
			>
				{[...maze]
					.sort((a, b) => {
						if (a.row !== b.row) return b.row - a.row;
						return a.col - b.col;
					})
					.map((cell) => (
						<div
							key={`${cell.row}-${cell.col}`}
							className={`cell ${cell.walls.map((w) => `wall-${w}`).join(" ")}`}
							style={{ width: cellSize, height: cellSize }}
						></div>
					))}
			</div>
		</div>
	);
}