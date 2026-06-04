// Verifies the 48 teams in index.html match exactly the 48 teams that
// qualified for the 2026 FIFA World Cup. Catches any drift / typos / missing
// or ghost teams.
//
// Run: node test_teams.js

const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const m = html.match(/const POTS = \{[\s\S]*?\};/);
if (!m) { console.error('FAIL: POTS not found in index.html'); process.exit(1); }
const POTS = (new Function(m[0] + '\nreturn POTS;'))();

// Definitive 48-team list for the 2026 FIFA World Cup.
// Source: Wikipedia + FIFA, cross-checked June 2026 (post-March playoffs).
// Names normalised to the spellings used in index.html.
const QUALIFIED = new Set([
  // Pot 1 (top-ranked)
  'France', 'Spain', 'Argentina', 'England', 'Portugal', 'Brazil',
  'Netherlands', 'Morocco', 'Belgium', 'Germany', 'Croatia', 'Colombia',
  // Pot 2
  'Senegal', 'Mexico', 'USA', 'Uruguay', 'Japan', 'Switzerland',
  'Iran', 'Türkiye', 'Ecuador', 'Austria', 'South Korea', 'Australia',
  // Pot 3
  'Algeria', 'Egypt', 'Canada', 'Norway', 'Panama', 'Ivory Coast',
  'Sweden', 'Paraguay', 'Czechia', 'Scotland', 'Tunisia', 'DR Congo',
  // Pot 4
  'Uzbekistan', 'Qatar', 'Iraq', 'South Africa', 'Saudi Arabia', 'Jordan',
  'Bosnia & Herzegovina', 'Cape Verde', 'Ghana', 'Curaçao', 'Haiti', 'New Zealand',
]);

const inPots = [];
for (const pot of Object.keys(POTS)) {
  for (const team of POTS[pot]) inPots.push(team);
}

let failures = 0;
function check(label, cond, detail = '') {
  console.log(`  ${cond ? 'PASS' : 'FAIL'}  ${label}${detail ? ' — ' + detail : ''}`);
  if (!cond) failures++;
}

console.log('\n── Team-pool integrity ──');
check(`exactly 48 teams in pots (got ${inPots.length})`, inPots.length === 48);
check(`no duplicates`, new Set(inPots).size === inPots.length);
check(`expected reference set has 48`, QUALIFIED.size === 48);

const inPotsSet = new Set(inPots);
const missing = [...QUALIFIED].filter(t => !inPotsSet.has(t));
const ghosts  = [...inPotsSet].filter(t => !QUALIFIED.has(t));
check(`no missing qualified teams`, missing.length === 0, missing.join(', '));
check(`no ghost teams`, ghosts.length === 0, ghosts.join(', '));

console.log('\n── Pot sizes ──');
for (const pot of Object.keys(POTS)) {
  check(`${pot} has 12 teams`, POTS[pot].length === 12,
    `got ${POTS[pot].length}`);
}

console.log('\n── Spot-check qualified / not-qualified ──');
// Notable teams that did NOT qualify in 2026 — must be absent from pots.
const NOT_QUALIFIED = ['Italy', 'Nigeria', 'Denmark', 'Hungary', 'Poland',
  'Serbia', 'Wales', 'Ukraine', 'Cameroon', 'Russia', 'Chile', 'Peru'];
let absentOk = true;
let stowaways = [];
for (const t of NOT_QUALIFIED) {
  if (inPotsSet.has(t)) { absentOk = false; stowaways.push(t); }
}
check('no unqualified teams in pots', absentOk, stowaways.join(', '));

// Notable confirmed qualifiers — must be present.
const MUST_HAVE = ['USA', 'Mexico', 'Canada', 'France', 'England', 'Cape Verde',
  'Curaçao', 'New Zealand', 'Uzbekistan', 'Jordan', 'DR Congo', 'Iraq'];
let presentOk = true;
let missingNotable = [];
for (const t of MUST_HAVE) {
  if (!inPotsSet.has(t)) { presentOk = false; missingNotable.push(t); }
}
check('all confirmed qualifiers present', presentOk, missingNotable.join(', '));

console.log('\n── Flag code coverage ──');
const codeMatch = html.match(/const TEAM_CODES = \{[\s\S]*?\};/);
let codes = {};
if (codeMatch) codes = (new Function(codeMatch[0] + '\nreturn TEAM_CODES;'))();
const missingCodes = inPots.filter(t => !codes[t]);
check('every team has a flag code', missingCodes.length === 0, missingCodes.join(', '));
check('no orphan flag codes', Object.keys(codes).every(k => inPotsSet.has(k)),
  Object.keys(codes).filter(k => !inPotsSet.has(k)).join(', '));

console.log('\n──────────────────────────');
if (failures === 0) {
  console.log('ALL CHECKS PASSED ✓ — team pool matches the actual 48-team World Cup field');
  process.exit(0);
} else {
  console.log(`${failures} CHECK(S) FAILED`);
  process.exit(1);
}
