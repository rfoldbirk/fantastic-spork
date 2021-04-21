const { execSync } = require('child_process')
let string = process.argv[2].split('').join(' ')
string.replace(' : d ', ' 0xff08 ')
string.replace(' : r ', ' 0xff0d ')

console.log(string)
execSync(`DISPLAY=:0 xdotool key ${ string }`)