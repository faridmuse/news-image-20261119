// main.ts — entry point for the news-image-20261119 make.fun submission.
//
// The grader runs `node /bot/main.ts` from an arbitrary working directory
// with no network and a read-only /bot. This script therefore resolves
// entry.png relative to its own location (not process.cwd()), creates the
// output directory named by MAKEFUN_OUTPUT_DIR (default "out"), and copies
// entry.png there. Plain Node ESM stdlib only; no TypeScript-only syntax,
// so it runs under node22 type-stripping.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(scriptDir, "entry.png");

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const outputPath = join(outputDir, "entry.png");

if (!existsSync(sourcePath)) {
  console.error(`entry.png not found next to main.ts: ${sourcePath}`);
  console.error("Regenerate it with: python3 draw-20261119.py");
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourcePath, outputPath);
console.log(`copied entry.png -> ${outputPath}`);
