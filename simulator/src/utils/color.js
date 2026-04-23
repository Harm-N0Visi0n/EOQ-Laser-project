export function blendRgbw([r = 0, g = 0, b = 0, w = 0]) {
  return [Math.min(255, r + w), Math.min(255, g + w), Math.min(255, b + w)]
}

export function rgbwToCss(color, fallback = '#111418') {
  const [cr, cg, cb] = blendRgbw(color)
  return (cr + cg + cb === 0) ? fallback : `rgb(${cr},${cg},${cb})`
}
