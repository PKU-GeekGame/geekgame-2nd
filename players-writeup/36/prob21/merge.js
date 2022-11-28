const part1 = require('./sheet1.json');
const part2 = require('./sheet2.json');

let url = []

for (let key in part1) {
    url.push(part1[key][2][1])
}

for (let key in part2) {
    url.push(part2[key][2][1])
}

console.log(url.join(''))
