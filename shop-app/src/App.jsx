import { useState } from 'react'

// ---- Product data ----
const PRODUCTS = [
  { slug: 'trailpack-40l', name: 'TrailPack 40L', price: 129.0 },
  { slug: 'summit-tent-2p', name: 'Summit Tent 2P', price: 219.0 },
  { slug: 'ember-camp-stove', name: 'Ember Camp Stove', price: 54.5 },
  { slug: 'trekking-poles', name: 'Driftwood Trekking Poles', price: 78.0 },
]

const VALID_USER = { username: 'standard_user', password: 'secret_sauce' }

export default function App() {
  // "step" drives which screen is shown - simpler than a router for a small app
  const [step, setStep] = useState('login') // login | products | cart | checkout | complete
  const [cart, setCart] = useState([]) // [{ slug, name, price, qty }]
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

  return (
    <div className="min-h-screen bg-sand-50">
      {step !== 'login' && (
        <header className="border-b border-moss-200 bg-white px-6 py-4 flex justify-between items-center">
          <button onClick={() => setStep('products')} className="font-semibold text-moss-800">
            TrekKart
          </button>
          <button
            id="cart-link"
            onClick={() => setStep('cart')}
            className="text-sm text-moss-700"
          >
            Cart ({cartCount})
          </button>
        </header>
      )}

      <main className="max-w-md mx-auto px-6 py-10">
        {/* ---- LOGIN ---- */}
        {step === 'login' && (
          <form onSubmit={handleLogin} className="bg-white border border-moss-200 rounded-lg p-6 space-y-4">
            <h1 className="text-xl font-semibold text-center mb-2">TrekKart</h1>
            <div>
              <label htmlFor="user-name" className="block text-sm mb-1">Username</label>
              <input id="user-name" name="username" className="w-full border border-moss-200 rounded px-3 py-2 text-sm" />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm mb-1">Password</label>
              <input id="password" name="password" type="password" className="w-full border border-moss-200 rounded px-3 py-2 text-sm" />
            </div>
            {loginError && <p className="text-sm text-red-600">{loginError}</p>}
            <button id="login-button" type="submit" className="w-full bg-moss-700 text-white rounded py-2 text-sm">
              Log in
            </button>
            <p className="text-xs text-center text-moss-400">standard_user / secret_sauce</p>
          </form>
        )}

        {/* ---- PRODUCTS ---- */}
        {step === 'products' && (
          <div className="inventory_list space-y-3">
            <h1 className="text-xl font-semibold mb-4">Gear</h1>
            {PRODUCTS.map((p) => (
              <div key={p.slug} className="inventory_item bg-white border border-moss-200 rounded-lg p-4 flex justify-between items-center">
                <div>
                  <p className="inventory_item_name font-medium">{p.name}</p>
                  <p className="inventory_item_price text-sm text-moss-600">${p.price.toFixed(2)}</p>
                </div>
                <button
                  id={`add-to-cart-${p.slug}`}
                  onClick={() => addToCart(p)}
                  className="btn_inventory bg-clay-500 text-white text-sm rounded px-3 py-1.5"
                >
                  Add
                </button>
              </div>
            ))}
          </div>
        )}

        {/* ---- CART ---- */}
        {step === 'cart' && (
          <div>
            <h1 className="text-xl font-semibold mb-4">Cart</h1>
            {cart.length === 0 ? (
              <p className="text-moss-500 text-sm">Your cart is empty.</p>
            ) : (
              <>
                <div className="cart_list space-y-2 mb-4">
                  {cart.map((i) => (
                    <div key={i.slug} className="cart_item bg-white border border-moss-200 rounded-lg p-3 flex justify-between items-center">
                      <span className="inventory_item_name text-sm">{i.name} × {i.qty}</span>
                      <button onClick={() => removeFromCart(i.slug)} className="text-xs text-moss-400">Remove</button>
                    </div>
                  ))}
                </div>
                <button
                  id="checkout"
                  onClick={() => setStep('checkout')}
                  className="w-full bg-moss-700 text-white rounded py-2 text-sm"
                >
                  Checkout
                </button>
              </>
            )}
          </div>
        )}

        {/* ---- CHECKOUT / SUMMARY ---- */}
        {step === 'checkout' && (
          <div className="summary_info bg-white border border-moss-200 rounded-lg p-6">
            <h1 className="text-xl font-semibold mb-4">Order Summary</h1>
            <div className="space-y-1 text-sm mb-4">
              {cart.map((i) => (
                <div key={i.slug} className="flex justify-between">
                  <span>{i.name} × {i.qty}</span>
                  <span>${(i.price * i.qty).toFixed(2)}</span>
                </div>
              ))}
            </div>
            <div className="border-t border-moss-200 pt-3 space-y-1 text-sm">
              <div className="flex justify-between text-moss-600">
                <span>Item total</span><span>${itemTotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-moss-600">
                <span>Tax</span><span>${tax.toFixed(2)}</span>
              </div>
              <div className="summary_total_label flex justify-between font-semibold text-base pt-1">
                <span>Total</span><span>${total.toFixed(2)}</span>
              </div>
            </div>
            <button
              id="finish"
              onClick={() => { setCart([]); setStep('complete') }}
              className="w-full bg-clay-500 text-white rounded py-2 text-sm mt-5"
            >
              Finish
            </button>
          </div>
        )}

        {/* ---- COMPLETE ---- */}
        {step === 'complete' && (
          <div className="text-center">
            <h1 className="complete-header text-xl font-semibold mb-2">Thank you for your order!</h1>
            <button onClick={() => setStep('products')} className="text-sm text-clay-600 mt-4">
              Back to shop
            </button>
          </div>
        )}
      </main>
    </div>
  )
}