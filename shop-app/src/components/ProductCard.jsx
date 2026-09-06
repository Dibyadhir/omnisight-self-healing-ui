import { Link } from 'react-router-dom'
import { useCart } from './context/cartcontext'

export default function ProductCard({ product }) {
  const { addToCart, items } = useCart()
  const inCart = items.some((i) => i.slug === product.slug)

  return (
    <div className="inventory_item bg-parchment-50 border border-ridge-800/10 rounded-lg p-4 flex flex-col">
      <Link to={`/products/${product.slug}`} className="block mb-3">
        <div className="aspect-square bg-ridge-50 rounded-md flex items-center justify-center text-ridge-800/30 text-xs font-stamp uppercase tracking-wide">
          {product.category}
        </div>
      </Link>
      <Link to={`/products/${product.slug}`}>
        <p className="inventory_item_name font-medium text-ridge-800 hover:text-blaze-amber transition-colors">
          {product.name}
        </p>
      </Link>
      <p className="inventory_item_price text-sm text-ridge-800/60 font-stamp mb-3">
        ${product.price.toFixed(2)}
      </p>
      <button
        id={`add-to-cart-${product.slug}`}
        onClick={() => addToCart(product)}
        disabled={inCart}
        className={`btn_inventory mt-auto text-sm font-medium rounded-md px-4 py-2 transition-colors ${
          inCart
            ? 'bg-ridge-50 text-ridge-800/40 cursor-not-allowed'
            : 'bg-blaze-amber hover:bg-blaze-rust text-white'
        }`}
      >
        {inCart ? 'Added' : 'Add to Cart'}
      </button>
    </div>
  )
}
