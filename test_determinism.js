// Determinism test for the World Cup Sweepstake draw.
// Loads index.html, extracts the deterministic RNG/shuffle/draw-plan code,
// and verifies that the draw is reproducible across "runs" (i.e. devices).
//
// Run: node test_determinism.js

const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) { console.error('FAIL: no <script> in index.html'); process.exit(1); }
const script = scriptMatch[1];

// Pull out the deterministic chunks: POTS, N_PLAYERS, mulberry32, seededShuffle, buildDrawPlan
function extract(name, pattern) {
  const m = script.match(pattern);
  if (!m) throw new Error(`Could not extract ${name}`);
  return m[0];
}

const chunks = [
  extract('POTS',           /const POTS = \{[\s\S]*?\};/),
  extract('POT_NAMES',      /const POT_NAMES = Object\.keys\(POTS\);/),
  extract('N_PLAYERS',      /const N_PLAYERS = 12;/),
  extract('mulberry32',     /function mulberry32\(seed\) \{[\s\S]*?\n\}/),
  extract('seededShuffle',  /function seededShuffle\(arr, rng\) \{[\s\S]*?\n\}/),
  extract('buildDrawPlan',  /function buildDrawPlan\(players, seed\) \{[\s\S]*?\n\}/),
];

const sandboxCode = chunks.join('\n\n') + `
module.exports = { POTS, POT_NAMES, N_PLAYERS, mulberry32, seededShuffle, buildDrawPlan };
`;

// Eval in this process
const Module = require('module');
const m = new Module('sandbox');
m._compile(sandboxCode, 'sandbox.js');
const { POTS, POT_NAMES, N_PLAYERS, buildDrawPlan } = m.exports;

let failures = 0;
function check(name, cond, detail = '') {
  if (cond) {
    console.log(`  PASS  ${name}`);
  } else {
    console.log(`  FAIL  ${name}${detail ? ' — ' + detail : ''}`);
    failures++;
  }
}

const players = ['Alice','Bob','Charlie','Dave','Eve','Frank','Grace','Heidi','Ivan','Judy','Karl','Liam'];

console.log('\n── Test 1: same seed + players → identical plan ──');
const seed = 0xDEADBEEF;
const p1 = buildDrawPlan(players, seed);
const p2 = buildDrawPlan(players, seed);
check('player order matches',
  JSON.stringify(p1.playerOrder) === JSON.stringify(p2.playerOrder));
check('queue matches (all 48 picks)',
  JSON.stringify(p1.queue) === JSON.stringify(p2.queue));
check('pot shuffles match',
  JSON.stringify(p1.potShuffles) === JSON.stringify(p2.potShuffles));

console.log('\n── Test 2: 1000 independent runs with same seed are bit-identical ──');
let bitwiseStable = true;
const reference = JSON.stringify(buildDrawPlan(players, seed));
for (let i = 0; i < 1000; i++) {
  if (JSON.stringify(buildDrawPlan(players, seed)) !== reference) {
    bitwiseStable = false; break;
  }
}
check('1000 reruns identical', bitwiseStable);

console.log('\n── Test 3: different seeds → different plans ──');
const pA = buildDrawPlan(players, 1);
const pB = buildDrawPlan(players, 2);
check('seed 1 ≠ seed 2',
  JSON.stringify(pA.queue) !== JSON.stringify(pB.queue));

console.log('\n── Test 4: every player gets exactly 1 team from each pot ──');
const plan = buildDrawPlan(players, seed);
const playerAlloc = {};
players.forEach(p => playerAlloc[p] = { picks: [], pots: new Set() });
plan.queue.forEach(item => {
  playerAlloc[item.player].picks.push(item.team);
  playerAlloc[item.player].pots.add(item.pot);
});
let allocOk = true;
let allocDetail = '';
for (const p of players) {
  if (playerAlloc[p].picks.length !== 4) { allocOk = false; allocDetail = `${p} got ${playerAlloc[p].picks.length}`; break; }
  if (playerAlloc[p].pots.size !== 4)    { allocOk = false; allocDetail = `${p} got pots ${[...playerAlloc[p].pots]}`; break; }
}
check('every player: 4 teams, 1 per pot', allocOk, allocDetail);

console.log('\n── Test 5: all 48 teams used exactly once ──');
const allTeams = [];
POT_NAMES.forEach(pn => POTS[pn].forEach(t => allTeams.push(t)));
const allocatedTeams = plan.queue.map(q => q.team);
const allocatedSorted = [...allocatedTeams].sort();
const poolSorted = [...allTeams].sort();
check(`48 teams allocated (got ${allocatedTeams.length})`, allocatedTeams.length === 48);
check('no duplicates in allocation', new Set(allocatedTeams).size === 48);
check('allocated set === pool set', JSON.stringify(allocatedSorted) === JSON.stringify(poolSorted));

console.log('\n── Test 6: pot 1 winners come from pot 1, etc. ──');
let potIntegrityOk = true;
plan.queue.forEach(item => {
  if (!POTS[item.pot].includes(item.team)) potIntegrityOk = false;
});
check('every pick is from its declared pot', potIntegrityOk);

console.log('\n── Test 7: ranking-order assumption (Pot 1 = top 12 ranked teams) ──');
// Spot-check: Pot 1 contains France and Spain (top 2), Pot 4 contains New Zealand (lowest)
check('Pot 1 has France', POTS[POT_NAMES[0]].includes('France'));
check('Pot 1 has Spain', POTS[POT_NAMES[0]].includes('Spain'));
check('Pot 1 has Argentina', POTS[POT_NAMES[0]].includes('Argentina'));
check('Pot 4 has New Zealand', POTS[POT_NAMES[3]].includes('New Zealand'));
check('Pot 4 has Haiti', POTS[POT_NAMES[3]].includes('Haiti'));
check('USA is in Pot 2 (rank 16, not auto-Pot1)', POTS[POT_NAMES[1]].includes('USA'));

console.log('\n── Test 8: seed range — 1000 random seeds all produce valid plans ──');
let randomSeedOk = true;
let badSeed = null;
for (let i = 0; i < 1000; i++) {
  const s = Math.floor(Math.random() * 0xFFFFFFFF);
  const pp = buildDrawPlan(players, s);
  if (pp.queue.length !== 48) { randomSeedOk = false; badSeed = s; break; }
  const set = new Set(pp.queue.map(q => q.team));
  if (set.size !== 48) { randomSeedOk = false; badSeed = s; break; }
}
check('1000 random seeds all produce valid 48-pick plans', randomSeedOk,
  badSeed !== null ? `bad seed: ${badSeed}` : '');

console.log('\n── Test 9: re-derive plan from URL-encoded seed (hex round-trip) ──');
const originalSeed = 0xABCDEF12;
const hexSeed = originalSeed.toString(16);
const decodedSeed = parseInt(hexSeed, 16);
const planA = buildDrawPlan(players, originalSeed);
const planB = buildDrawPlan(players, decodedSeed);
check('hex round-trip preserves plan',
  JSON.stringify(planA) === JSON.stringify(planB));

console.log('\n── Test 10: player name order in URL does not matter for outcomes ──');
// The shuffle uses the player array as-is, so name order DOES matter (intentionally).
// This is just confirming the property — different input order = different shuffle.
const reversed = players.slice().reverse();
const planForward = buildDrawPlan(players, seed);
const planReversed = buildDrawPlan(reversed, seed);
check('different input order → different player order (as expected)',
  JSON.stringify(planForward.playerOrder) !== JSON.stringify(planReversed.playerOrder));

console.log('\n──────────────────────────');
if (failures === 0) {
  console.log(`ALL ${failures === 0 ? 'tests passed' : 'tests failed'} ✓`);
  process.exit(0);
} else {
  console.log(`${failures} test(s) FAILED`);
  process.exit(1);
}
