// gta6-meme-x-01 entry (Node 22, standard library only).
//
// It copies POST.json from the repository root to /output/POST.json, where
// the gate reads it. That is all the program has to do. The entry is the
// post itself: the meme was made in this session, it is posted on X from a
// public account with make.fun (a link) and @makefunai and the play code in
// its text, POST.json names the post, and the house reads the post from X
// (its first picture and its text) and hands that to the judge. Nothing
// this program writes about the post is judged.
//
// POST.json currently holds a placeholder address, so the gate refuses it
// as it stands (valid 0). The coordinator replaces it with the real post
// address after the user posts the meme on X, then commits again.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The entry is the post itself, so this program is deliberately tiny and
// deterministic: same input bytes in, same bytes out, on every run. It
// only checks that POST.json parses as a JSON object before copying it,
// so a typo in the post address fails loudly here instead of at the gate.
function handInPost(): void {
  const source = join(BOT_DIR, 'POST.json');
  const parsed: unknown = JSON.parse(readFileSync(source, 'utf8'));
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    throw new Error('POST.json must be a JSON object like {"url": "https://x.com/<handle>/status/<id>"}');
  }
  mkdirSync(OUTPUT_DIR, { recursive: true });
  copyFileSync(source, join(OUTPUT_DIR, 'POST.json'));
}

try {
  handInPost();
} catch (err) {
  console.error(`POST.json could not be handed in from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
