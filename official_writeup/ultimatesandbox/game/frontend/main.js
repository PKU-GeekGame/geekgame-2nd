/** @type {HTMLInputElement} */
const display = document.querySelector('.display')

const SPECIAL = {
  C: () => (display.value = ''),
  '⬅': () =>
    (display.value = display.value.substring(0, display.value.length - 1)),
  '=': () => {
    try {
      display.value = eval(display.value)
    } catch {
      alert('Invalid Expression')
    }
  },
  '÷': '/',
  '×': '*'
}

const buttons = document.querySelectorAll('.calc-btn')
for (const button of buttons) {
  const op = button.textContent.trim()
  if (op in SPECIAL) {
    const alt = SPECIAL[op]
    switch (typeof alt) {
      case 'string':
        button.addEventListener('click', () => (display.value += alt))
        break
      case 'function':
        button.addEventListener('click', alt)
        break
    }
  } else {
    button.addEventListener('click', () => (display.value += op))
  }
}

if (localStorage.getItem('i_am_premium_user') === 'true') {
  import('./main-premium.js')
}
