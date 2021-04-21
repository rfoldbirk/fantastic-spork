const { execSync } = require('child_process')
const string = process.argv[2].split('').join(' ')
execSync(`DISPLAY=:0 xdotool key ${ string }`)