import { Link } from 'react-router-dom'
import Header from './components/header'
import ProductCard from './components/productcard'
import { useCart } from './context/cartcontext'

export default function HomePage() {
  const { PRODUCTS } = useCart()
  const featured = PRODUCTS.slice(0, 3)

  return (
    <div className="min-h-screen bg-parchment-100">
      <Header />

      {/* Hero */}
      <section className="border-b border-ridge-800/10">
        <div className="max-w-5xl mx-auto px-6 py-16 text-center">
          <p className="font-stamp text-[10px] uppercase tracking-[0.2em] text-blaze-amber mb-3">
            New Season Gear
          </p>
          <h1 className="font-display italic text-4xl sm:text-5xl font-semibold text-ridge-800 mb-4">
            Gear for the way there.
          </h1>
          <p className="text-ridge-800/60 max-w-md mx-auto mb-8">
            Trail-tested packs, shelters, and tools built to hold up past the trailhead.
          </p>
          <Link
            to="/products"
            className="inline-block bg-ridge-800 hover:bg-ridge-900 text-parchment-50 font-medium rounded-md px-6 py-3 text-sm transition-colors"
          >
            Shop All Gear
          </Link>
        </div>
      </section>

      {/* Featured products - reuses the same .inventory_list / .inventory_item
          markup as the full Products page, so existing automation scripts
          that look for these classes right after login still find them here. */}
      <section className="max-w-5xl mx-auto px-6 py-12">
        <div className="flex items-center justify-between mb-5">
          <h2 className="font-display italic text-2xl font-semibold text-ridge-800">
            Featured Gear
          </h2>
          <Link to="/products" className="font-stamp text-xs uppercase tracking-wide text-blaze-amber hover:text-blaze-rust">
            View all
          </Link>
        </div>
        <div className="inventory_list grid grid-cols-1 sm:grid-cols-3 gap-5">
          {featured.map((p) => (
            <ProductCard key={p.slug} product={p} />
          ))}
        </div>
      </section>
    </div>
  )
}
