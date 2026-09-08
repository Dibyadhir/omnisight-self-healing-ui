export function Blaze({ state }) {
  const styles = {
    done: 'bg-ridge-700 border-ridge-700',
    current: 'bg-blaze-amber border-blaze-amber',
    upcoming: 'bg-transparent border-ridge-200',
  }
  return <span className={`block w-3 h-5 rounded-[2px] border-2 ${styles[state]}`} />
}

const TRAIL_STEPS = [
  { key: '/products', label: 'Gear' },
  { key: '/cart', label: 'Cart' },
  { key: '/checkout', label: 'Checkout' },
  { key: '/checkout-complete', label: 'Done' },
]

export function TrailIndicator({ currentPath }) {
  const currentIndex = TRAIL_STEPS.findIndex((s) => s.key === currentPath)
  return (
    <div className="max-w-md mx-auto px-6 pt-6">
      <div className="flex items-center">
        {TRAIL_STEPS.map((s, i) => (
          <div key={s.key} className="flex items-center flex-1 last:flex-none">
            <div className="flex flex-col items-center gap-1.5">
              <Blaze state={i < currentIndex ? 'done' : i === currentIndex ? 'current' : 'upcoming'} />
              <span
                className={`font-stamp text-[10px] uppercase tracking-wider ${
                  i === currentIndex ? 'text-blaze-amber' : 'text-ridge-800/40'
                }`}
              >
                {s.label}
              </span>
            </div>
            {i < TRAIL_STEPS.length - 1 && (
              <div
                className={`flex-1 h-px mx-2 mb-4 border-t-2 border-dashed ${
                  i < currentIndex ? 'border-ridge-700' : 'border-ridge-200'
                }`}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export function TrailMark() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" className="text-blaze-amber shrink-0">
      <path d="M2 20L9 8l4 6.5L16 10l6 10H2z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
    </svg>
  )
}

export { TRAIL_STEPS }