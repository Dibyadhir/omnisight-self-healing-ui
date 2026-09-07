import { useNavigate, useLocation } from 'react-router-dom'
import Header from '../components/Header'
import { TrailIndicator } from '../components/TrailBlaze'
import { useCart } from '../context/CartContext'

export default function CheckoutPage() {
  const { items, itemTotal, tax, total, clearCart } = useCart()
  const navigate = useNavigate()
  const location = useLocation()

  function handleFinish() {
    clearCart()
    navigate('/checkout-complete')
  }

  return (
    <div className="min-h-screen bg-parchment-100 flex flex-col">
      <Header />
      <TrailIndicator currentPath={location.pathname} />
      <main className="flex-1 max-w-md w-full mx-auto px-6 py-8">
        <h1 className="font-display italic text-2xl font-semibold text-ridge-800 mb-5">Order Summary</h1>
        <div className="summary_info bg-parchment-50 border border-ridge-800/10 rounded-lg p-6">
          <div className="space-y-2 text-sm mb-5">
            {items.map((i) => (
              <div key={i.slug} className="cart_item flex justify-between text-ridge-800">
                <span className="inventory_item_name">{i.name} × {i.qty}</span>
                <span className="inventory_item_price font-stamp">${(i.price * i.qty).toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="border-t border-dashed border-ridge-800/20 pt-4 space-y-1.5 text-sm">
            <div className="summary_subtotal_label flex justify-between text-ridge-800/60">
              <span>Item total</span><span className="font-stamp">${itemTotal.toFixed(2)}</span>
            </div>
            <div className="summary_tax_label flex justify-between text-ridge-800/60">
              <span>Tax</span><span className="font-stamp">${tax.toFixed(2)}</span>
            </div>
            <div className="summary_total_label flex justify-between font-semibold text-ridge-800 text-base pt-1.5">
              <span>Total</span><span className="font-stamp">${total.toFixed(2)}</span>
            </div>
          </div>
          <button
            id="finish"
            onClick={handleFinish}
            className="w-full bg-blaze-amber hover:bg-blaze-rust text-white font-medium rounded-md py-2.5 text-sm mt-6 transition-colors"
          >
            Finish
          </button>
        </div>
      </main>
    </div>
  )
}