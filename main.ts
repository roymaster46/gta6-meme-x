// gta6-meme-x-01 entry, v2 (Node 22, standard library only).
//
// It hands in the X post this entry is about: POST.json (the post's
// address) and POST_TEXT.txt (the exact text that was posted) are copied
// to /output/, where the gate reads them. The entry is the post itself:
// the meme was made in this session, it is posted on X from a public
// account with make.fun (a link) and @makefunai and the play code in its
// text, POST.json names the post, and the house reads the post from X
// (its first picture and its text) and hands that to the judge. Nothing
// this program writes about the post is judged.
//
// v2 changes the meme, not the plumbing: the flat beach photo ("still
// waiting") is replaced by a fake official document — a Steam invoice
// for a GTA VI pre-order placed 17 Sep 2013 and finally DELIVERED
// 19 Nov 2026, 13 years, 2 months, 2 days (4,811 days) late, with a
// $0.00 late fee. The board's winners all play the 13-year wait through
// a specific bureaucratic format; this one does the same, with the
// delivery time as the punchline.
//
// POST.json currently holds the v1 post address; the coordinator replaces
// it with the v2 post address after the user posts the new meme on X,
// then commits again.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The meme this entry posts. v1 used meme.png (the beach photo); v2
// posts meme-v2.png (the Steam invoice). The file must be present in the
// repository, or the post the entry claims cannot exist.
const MEME_FILE = 'meme-v2.png';

// An X status address looks like https://x.com/<handle>/status/<digits>.
// A placeholder or a non-status link fails loudly here instead of at
// the gate.
const STATUS_URL = /^https:\/\/x\.com\/[A-Za-z0-9_]+\/status\/\d+$/;

// The entry is the post itself, so this program is deliberately tiny and
// deterministic: same input bytes in, same bytes out, on every run. It
// only checks that the handoff files are well formed before copying
// them, so a typo in the post address fails loudly here instead of at
// the gate.
function handInPost(): void {
  const postPath = join(BOT_DIR, 'POST.json');
  const parsed: unknown = JSON.parse(readFileSync(postPath, 'utf8'));
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    throw new Error('POST.json must be a JSON object like {"url": "https://x.com/<handle>/status/<id>"}');
  }
  const url = (parsed as Record<string, unknown>).url;
  if (typeof url !== 'string' || !STATUS_URL.test(url)) {
    throw new Error(`POST.json url must be an X status address, got: ${String(url)}`);
  }
  const textPath = join(BOT_DIR, 'POST_TEXT.txt');
  if (!existsSync(textPath)) {
    throw new Error('POST_TEXT.txt is missing: the exact posted text must be in the repository');
  }
  // The bounty requires three things in the post text: the bounty link,
  // @makefunai, and the play code. If any is missing the gate refuses
  // the entry, so check here while the mistake is still cheap to fix.
  const text = readFileSync(textPath, 'utf8');
  const required = [
    'https://make.fun/bounty/gta6-meme-x-01',
    '@makefunai',
    'makefun-dormouse-granola-rosemary',
  ];
  for (const needle of required) {
    if (!text.includes(needle)) {
      throw new Error(`POST_TEXT.txt is missing a required element: ${needle}`);
    }
  }
  // X counts a non-Premium post at 280 characters. The file has no
  // trailing newline; count what would actually be posted.
  if (text.replace(/\r\n/g, '\n').length > 280) {
    throw new Error(`POST_TEXT.txt is ${text.length} characters, over the 280 limit for a non-Premium post`);
  }
  const memePath = join(BOT_DIR, MEME_FILE);
  if (!existsSync(memePath)) {
    throw new Error(`${MEME_FILE} is missing: the meme this entry posts must be in the repository`);
  }
  mkdirSync(OUTPUT_DIR, { recursive: true });
  copyFileSync(postPath, join(OUTPUT_DIR, 'POST.json'));
  copyFileSync(textPath, join(OUTPUT_DIR, 'POST_TEXT.txt'));
}

try {
  handInPost();
} catch (err) {
  console.error(`POST.json could not be handed in from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
