import { useNavigate, useLocation } from 'react-router-dom'
import Header from '../components/Header'
import { TrailIndicator } from '../components/TrailBlaze'
import { useCart } from '../context/CartContext'

export default function CartPage() {
  const { items, removeFromCart } = useCart()
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <div className="min-h-screen bg-parchment-100 flex flex-col">
      <Header />
      <TrailIndicator currentPath={location.pathname} />
      <main className="flex-1 max-w-md w-full mx-auto px-6 py-8">
        <h1 className="font-display italic text-2xl font-semibold text-ridge-800 mb-5">Cart</h1>
        {items.length === 0 ? (
          <div className="bg-parchment-50 border border-dashed border-ridge-800/20 rounded-lg p-8 text-center">
            <p className="text-ridge-800/50 text-sm">Your pack is empty.</p>
          </div>
        ) : (
          <>
            <div className="cart_list space-y-2 mb-6">
              {items.map((i) => (
                <div
                  key={i.slug}
                  className="cart_item bg-parchment-50 border border-ridge-800/10 rounded-lg p-3.5 flex justify-between items-center"
                >
                  <span className="inventory_item_name text-sm text-ridge-800">
                    {i.name} <span className="cart_quantity text-ridge-800/40">× {i.qty}</span>
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
              onClick={() => navigate('/checkout')}
              className="w-full bg-ridge-800 hover:bg-ridge-900 text-parchment-50 font-medium rounded-md py-2.5 text-sm transition-colors"
            >
              Checkout
            </button>
          </>
        )}
      </main>
    </div>
  )
}