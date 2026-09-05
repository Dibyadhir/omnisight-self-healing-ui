import { useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import Header from './components/header'
import { useCart } from './context/cartcontext'

export default function ProductDetailPage() {
  const { slug } = useParams()
  const { PRODUCTS, addToCart } = useCart()
  const navigate = useNavigate()
  const [qty, setQty] = useState(1)

  const product = PRODUCTS.find((p) => p.slug === slug)

  if (!product) {
    return (
      <div className="min-h-screen bg-parchment-100">
        <Header />
        <main className="max-w-md mx-auto px-6 py-16 text-center">
          <p className="text-ridge-800/60 mb-4">We couldn't find that product.</p>
          <Link to="/products" className="text-blaze-amber font-stamp text-xs uppercase tracking-wide">
            Back to shop
          </Link>
        </main>
      </div>
    )
  }

  function handleAddToCart() {
    for (let i = 0; i < qty; i++) addToCart(product)
    navigate('/cart')
  }

  return (
    <div className="min-h-screen bg-parchment-100">
      <Header />
      <main className="max-w-3xl mx-auto px-6 py-10">
        <Link to="/products" className="font-stamp text-xs uppercase tracking-wide text-ridge-800/50 hover:text-ridge-800">
          &larr; Back to shop
        </Link>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 mt-6">
          <div className="aspect-square bg-ridge-50 rounded-lg flex items-center justify-center text-ridge-800/30 font-stamp uppercase tracking-wide text-sm">
            {product.category}
          </div>

          <div>
            <p className="font-stamp text-[10px] uppercase tracking-[0.15em] text-blaze-amber mb-2">
              {product.category}
            </p>
            <h1 className="product_detail_name font-display italic text-2xl font-semibold text-ridge-800 mb-3">
              {product.name}
            </h1>
            <p className="product_detail_price text-xl font-stamp text-ridge-800 mb-4">
              ${product.price.toFixed(2)}
            </p>
            <p className="product_detail_description text-ridge-800/70 text-sm leading-relaxed mb-6">
              {product.description}
            </p>

            <div className="flex items-center gap-3 mb-6">
              <label className="font-stamp text-xs uppercase tracking-wide text-ridge-800/60">Qty</label>
              <div className="flex items-center border border-ridge-800/15 rounded-md">
                <button
                  onClick={() => setQty((q) => Math.max(1, q - 1))}
                  className="px-3 py-1.5 text-ridge-800/60 hover:text-ridge-800"
                  aria-label="Decrease quantity"
                >
                  &minus;
                </button>
                <span className="px-3 text-sm font-stamp">{qty}</span>
                <button
                  onClick={() => setQty((q) => q + 1)}
                  className="px-3 py-1.5 text-ridge-800/60 hover:text-ridge-800"
                  aria-label="Increase quantity"
                >
                  +
                </button>
              </div>
            </div>

            <button
              id={`add-to-cart-${product.slug}`}
              onClick={handleAddToCart}
              className="btn_inventory w-full sm:w-auto bg-blaze-amber hover:bg-blaze-rust text-white font-medium rounded-md px-6 py-2.5 text-sm transition-colors"
            >
              Add to Cart
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}