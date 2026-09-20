// Preserve the existing root-level npm run slides entry point.
// Both formats and the replay now use the verified common content source.
const {spawnSync} = require('node:child_process');
const path = require('node:path');
const result = spawnSync('make', ['snapshot'], {
  cwd: path.resolve(__dirname, '..'), stdio: 'inherit'
});
if (result.error) { console.error(result.error.message); process.exit(1); }
process.exit(result.status === null ? 1 : result.status);
