import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const src = join(process.cwd(), "entry.png");
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error("entry.png not found — run: python3 draw-20261119.py");
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log(`copied entry.png -> ${dst}`);
