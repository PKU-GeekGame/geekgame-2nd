const flag0 = `flag{fr0nt3nd_log1c_m4tters}`
const [code, activate, status] = ['code', 'activate', 'status'].map((x) =>
  document.getElementById(x)
)
if (localStorage.getItem('i_am_premium_user')) {
  status.innerText = 'Premium Activated: ' + flag0
  code.disabled = true
  code.placeholder = 'Premium Activated'
  activate.disabled = true
  activate.innerText = 'You do not need to activate premium again'
} else {
  status.innerText = 'Not Activated'
  activate.addEventListener('click', () => {
    if (code.value === flag0) {
      alert('Welcome to premium!')
      localStorage.setItem('i_am_premium_user', true)
      location.reload()
    } else {
      alert('Ooooops your code is wrong {{{(>_<)}}}')
    }
  })
}
