const backend = document.getElementById('backend')
function appendOption(value, name) {
  const option = document.createElement('option')
  option.value = value
  option.textContent = name
  backend.appendChild(option)
}
appendOption('node', 'Node.JS')
appendOption('browser', 'Browser')

const original = [...document.querySelectorAll('.calc-btn')].find(
  (e) => e.textContent.trim() === '='
)
const submit = original.cloneNode(true)
submit.style.background = '#9b59b6'
submit.style.color = 'white'
original.replaceWith(submit)

const display = document.querySelector('.display')
submit.addEventListener('click', () => {
  const expr = display.value
  display.value = 'Calculating...'
  const mode = backend.value
  try {
    if (['node', 'browser'].includes(mode)) {
      fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expr, mode })
      })
        .then((res) => res.json())
        .then((res) => (display.value = '' + res.result))
    } else {
      display.value = eval(expr)
    }
  } catch (err) {
    console.log(err)
    display.value = 'Error'
  }
})
