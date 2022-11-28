const data = require('./data.json')

const maxcols = 11

let now = 0
result = []
curr = []
for (let key in data) {
    while (now < key) {
        curr.push('.')
        now++
        if (now % maxcols == 0) {
            result.push(curr.join(''))
            curr = []
        }
    }
    curr.push('#')
    now++
    if (now % maxcols == 0) {
        result.push(curr.join(''))
        curr = []
    }
}

console.log(result.join('\n'))

