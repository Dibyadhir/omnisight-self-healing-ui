import { useState } from 'react'

// ---- Product data ----
const PRODUCTS = [
  { slug: 'trailpack-40l', name: 'TrailPack 40L', price: 129.0 },
  { slug: 'summit-tent-2p', name: 'Summit Tent 2P', price: 219.0 },
  { slug: 'ember-camp-stove', name: 'Ember Camp Stove', price: 54.5 },
  { slug: 'trekking-poles', name: 'Driftwood Trekking Poles', price: 78.0 },
]

const VALID_USER = { username: 'standard_user', password: 'secret_sauce' }

// Steps a shopper walks through, in order - drives the trail-blaze indicator
const TRAIL_STEPS = [
  { key: 'products', label: 'Gear' },
  { key: 'cart', label: 'Cart' },
  { key: 'checkout', label: 'Checkout' },
  { key: 'complete', label: 'Done' },
]

// A single painted trail-blaze mark. Real trail blazes are rectangular paint
// marks on trees that hikers follow to stay on route - here they mark
// progress through checkout the same way.
function Blaze({ state }) {
  // state: 'done' | 'current' | 'upcoming'
  const styles = {
    done: 'bg-ridge-700 border-ridge-700',
    current: 'bg-blaze-amber border-blaze-amber',
    upcoming: 'bg-transparent border-ridge-200',
  }
  return <span className={`block w-3 h-5 rounded-[2px] border-2 ${styles[state]}`} />
}

function TrailIndicator({ step }) {
  const currentIndex = TRAIL_STEPS.findIndex((s) => s.key === step)
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

// Small mountain glyph used as the wordmark's icon - the one recurring motif
function TrailMark() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" className="text-blaze-amber shrink-0">
      <path d="M2 20L9 8l4 6.5L16 10l6 10H2z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
    </svg>
  )
}

export default function App() {
  const [step, setStep] = useState('login')
  const [cart, setCart] = useState([])
  const [loginError, setLoginError] = useState('')

  function handleLogin(e) {
    e.preventDefault()
    const form = new FormData(e.target)
    const username = form.get('username')
    const password = form.get('password')
    if (username === VALID_USER.username && password === VALID_USER.password) {
      setLoginError('')
      setStep('products')
    } else {
      setLoginError('Incorrect username or password.')
    }
  }

  function addToCart(product) {
    setCart((prev) => {
      const existing = prev.find((i) => i.slug === product.slug)
      if (existing) {
        return prev.map((i) => (i.slug === product.slug ? { ...i, qty: i.qty + 1 } : i))
      }
      return [...prev, { ...product, qty: 1 }]
    })
  }

  function removeFromCart(slug) {
    setCart((prev) => prev.filter((i) => i.slug !== slug))
  }

  const itemTotal = cart.reduce((sum, i) => sum + i.price * i.qty, 0)
  const tax = itemTotal * 0.08
  const total = itemTotal + tax
  const cartCount = cart.reduce((sum, i) => sum + i.qty, 0)

  // ---- LOGIN: full-height centered ----
  if (step === 'login') {
    return (
      <div className="min-h-screen flex items-center justify-center px-4 py-10 bg-parchment-100">
        <div className="w-full max-w-sm">
          <div className="flex items-center justify-center gap-2 mb-6">
            <TrailMark />
            <span className="font-display italic text-2xl font-semibold text-ridge-800 tracking-tight">
              TrekKart
            </span>
          </div>

          <form
            onSubmit={handleLogin}
            className="bg-parchment-50 border-2 border-ridge-800/10 rounded-xl p-7 shadow-[0_1px_0_0_theme(colors.ridge.800/8%)]"
          >
            <p className="font-stamp text-[10px] uppercase tracking-[0.15em] text-ridge-800/50 text-center mb-6">
              Trailhead Sign-In
            </p>

            <div className="mb-4">
              <label htmlFor="user-name" className="block text-sm font-medium text-ridge-800 mb-1.5">
                Username
              </label>
              <input
                id="user-name"
                name="username"
                autoComplete="username"
                className="w-full bg-white border border-ridge-800/15 rounded-md px-3 py-2.5 text-sm text-ridge-800 focus:border-blaze-amber transition-colors"
              />
            </div>
            <div className="mb-5">
              <label htmlFor="password" className="block text-sm font-medium text-ridge-800 mb-1.5">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                className="w-full bg-white border border-ridge-800/15 rounded-md px-3 py-2.5 text-sm text-ridge-800 focus:border-blaze-amber transition-colors"
              />
            </div>

            {loginError && (
              <p className="text-sm text-blaze-rust mb-4" role="alert">
                {loginError}
              </p>
            )}

            <button
              id="login-button"
              type="submit"
              className="w-full bg-ridge-800 hover:bg-ridge-900 text-parchment-50 font-medium rounded-md py-2.5 text-sm transition-colors"
            >
              Log in
            </button>

            <p className="font-stamp text-[10px] text-center text-ridge-800/40 mt-5 tracking-wide">
              standard_user / secret_sauce
            </p>
          </form>
        </div>
      </div>
    )
  }

  // ---- Everything past login shares a header + trail indicator ----
  return (
    <div className="min-h-screen bg-parchment-100 flex flex-col">
      <header className="border-b border-ridge-800/10 bg-parchment-50 px-6 py-4">
        <div className="max-w-md mx-auto flex items-center justify-between">
          <button
            onClick={() => setStep('products')}
            className="flex items-center gap-2 font-display italic font-semibold text-lg text-ridge-800"
          >
            <TrailMark />
            TrekKart
          </button>
          <button
            id="cart-link"
            onClick={() => setStep('cart')}
            className="font-stamp text-xs uppercase tracking-wide text-ridge-800/70 hover:text-ridge-800 flex items-center gap-1.5"
          >
            Cart
            <span className="bg-blaze-amber text-white text-[10px] font-semibold rounded-full w-5 h-5 flex items-center justify-center">
              {cartCount}
            </span>
          </button>
        </div>
      </header>

      {step !== 'complete' && <TrailIndicator step={step} />}

      <main className="flex-1 max-w-md w-full mx-auto px-6 py-8">
        {/* ---- PRODUCTS ---- */}
        {step === 'products' && (
          <div>
            <h1 className="font-display italic text-2xl font-semibold text-ridge-800 mb-5">Gear</h1>
            <div className="inventory_list space-y-3">
              {PRODUCTS.map((p) => (
                <div
                  key={p.slug}
                  className="inventory_item bg-parchment-50 border border-ridge-800/10 rounded-lg p-4 flex justify-between items-center"
                >
                  <div>
                    <p className="inventory_item_name font-medium text-ridge-800">{p.name}</p>
                    <p className="inventory_item_price text-sm text-ridge-800/60 font-stamp">
                      ${p.price.toFixed(2)}
                    </p>
                  </div>
                  <button
                    id={`add-to-cart-${p.slug}`}
                    onClick={() => addToCart(p)}
                    className="btn_inventory bg-blaze-amber hover:bg-blaze-rust text-white text-sm font-medium rounded-md px-4 py-2 transition-colors"
                  >
                    Add
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ---- CART ---- */}
        {step === 'cart' && (
          <div>
            <h1 className="font-display italic text-2xl font-semibold text-ridge-800 mb-5">Cart</h1>
            {cart.length === 0 ? (
              <div className="bg-parchment-50 border border-dashed border-ridge-800/20 rounded-lg p-8 text-center">
                <p className="text-ridge-800/50 text-sm">Your pack is empty.</p>
              </div>
            ) : (
              <>
                <div className="cart_list space-y-2 mb-6">
                  {cart.map((i) => (
                    <div
                      key={i.slug}
                      className="cart_item bg-parchment-50 border border-ridge-800/10 rounded-lg p-3.5 flex justify-between items-center"
                    >
                      <span className="inventory_item_name text-sm text-ridge-800">
                        {i.name} <span className="text-ridge-800/40">× {i.qty}</span>
                      </span>
                      <button
                        onClick={() => removeFromCart(i.slug)}
                        className="font-stamp text-[10px] uppercase tracking-wide text-ridge-800/40 hover:text-blaze-rust"
                      >
                        Remove
                      </button>
                    </div>
                  ))}
                </div>
                <button
                  id="checkout"
                  onClick={() => setStep('checkout')}
                  className="w-full bg-ridge-800 hover:bg-ridge-900 text-parchment-50 font-medium rounded-md py-2.5 text-sm transition-colors"
                >
                  Checkout
                </button>
              </>
            )}
          </div>
        )}

        {/* ---- CHECKOUT / SUMMARY ---- */}
        {step === 'checkout' && (
          <div>
            <h1 className="font-display italic text-2xl font-semibold text-ridge-800 mb-5">Order Summary</h1>
            <div className="summary_info bg-parchment-50 border border-ridge-800/10 rounded-lg p-6">
              <div className="space-y-2 text-sm mb-5">
                {cart.map((i) => (
                  <div key={i.slug} className="flex justify-between text-ridge-800">
                    <span>{i.name} × {i.qty}</span>
                    <span className="font-stamp">${(i.price * i.qty).toFixed(2)}</span>
                  </div>
                ))}
              </div>
              <div className="border-t border-dashed border-ridge-800/20 pt-4 space-y-1.5 text-sm">
                <div className="flex justify-between text-ridge-800/60">
                  <span>Item total</span><span className="font-stamp">${itemTotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-ridge-800/60">
                  <span>Tax</span><span className="font-stamp">${tax.toFixed(2)}</span>
                </div>
                <div className="summary_total_label flex justify-between font-semibold text-ridge-800 text-base pt-1.5">
                  <span>Total</span><span className="font-stamp">${total.toFixed(2)}</span>
                </div>
              </div>
              <button
                id="finish"
                onClick={() => { setCart([]); setStep('complete') }}
                className="w-full bg-blaze-amber hover:bg-blaze-rust text-white font-medium rounded-md py-2.5 text-sm mt-6 transition-colors"
              >
                Finish
              </button>
            </div>
          </div>
        )}

        {/* ---- COMPLETE ---- */}
        {step === 'complete' && (
          <div className="flex flex-col items-center text-center py-10">
            <div className="flex gap-1 mb-6">
              {TRAIL_STEPS.map((s) => <Blaze key={s.key} state="done" />)}
            </div>
            <h1 className="complete-header font-display italic text-2xl font-semibold text-ridge-800 mb-2">
              Thank you for your order!
            </h1>
            <p className="text-ridge-800/60 text-sm mb-6">Your gear is being packed for the trail.</p>
            <button
              onClick={() => setStep('products')}
              className="font-stamp text-xs uppercase tracking-wide text-blaze-amber hover:text-blaze-rust"
            >
              Back to shop
            </button>
          </div>
        )}
      </main>
    </div>
  )
}