// Hand-written entrypoint for the 19 November 2026 front page.
//
// What this does, in plain terms: it takes the finished newspaper image
// that lives next to this file (entry.png) and drops an exact copy of it
// into the output folder, creating that folder first if it is missing.
// The folder comes from MAKEFUN_OUTPUT_DIR when that variable is set,
// and falls back to /output otherwise.
//
// About the picture itself: it is the completed front page dated
// Thursday 19 November 2026 — a square 1024-by-1024 image, 187444 bytes
// on disk, carrying thirty-five numbered news stories alongside a world
// map and three photographs. This program does not redraw or alter any
// of that; it only moves the finished file into place, the same way
// every time, with no network access and no other files written.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const folderHere = dirname(fileURLToPath(import.meta.url));
const outputFolder = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outputFolder, { recursive: true });
copyFileSync(join(folderHere, "entry.png"), join(outputFolder, "entry.png"));
