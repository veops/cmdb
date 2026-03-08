import './highlight.less'

const escapeRegExp = (value) => {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

const escapeHtml = (value) => {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

const sanitizeClassName = (value) => {
  const className = value ? `${value}` : 'ops-text-highlight'
  return /^[A-Za-z0-9_-]+$/.test(className) ? className : 'ops-text-highlight'
}

const highlight = (el, binding) => {
  const options = (binding && binding.value) || {}
  if (options.value === undefined || options.value === null || `${options.value}` === '') {
    return
  }

  const text = escapeHtml(el.innerText || '')
  const keyword = escapeRegExp(`${options.value}`)
  const className = sanitizeClassName(options.class)
  const regex = new RegExp(`(${keyword})`, 'gi')
  el.innerHTML = text.replace(regex, `<span class='${className}'>$1</span>`)
}

export default highlight
