import { Link } from 'react-router-dom'
import { useCart } from './context/cartcontext'
import { TrailMark } from './TrailBlaze'

export default function Header() {
  const { items } = useCart()
  const cartCount = items.reduce((sum, i) => sum + i.qty, 0)

  return (
    <header className="border-b border-ridge-800/10 bg-parchment-50 px-6 py-4">
      <div className="max-w-5xl mx-auto flex items-center justify-between">
        <Link
          to="/home"
          className="flex items-center gap-2 font-display italic font-semibold text-lg text-ridge-800"
        >
          <TrailMark />
          TrekKart
        </Link>

        <nav className="hidden sm:flex items-center gap-6 font-stamp text-xs uppercase tracking-wide text-ridge-800/70">
          <Link to="/home" className="hover:text-ridge-800">Home</Link>
          <Link to="/products" className="hover:text-ridge-800">Shop</Link>
        </nav>

        <Link
          id="cart-link"
          to="/cart"
          className="shopping_cart_link font-stamp text-xs uppercase tracking-wide text-ridge-800/70 hover:text-ridge-800 flex items-center gap-1.5"
        >
          Cart
          <span className="bg-blaze-amber text-white text-[10px] font-semibold rounded-full w-5 h-5 flex items-center justify-center">
            {cartCount}
          </span>
        </Link>
      </div>
    </header>
  )
}
