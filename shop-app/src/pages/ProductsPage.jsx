import Header from './components/header'
import ProductCard from '../components/productcard '
import { TrailIndicator } from '../components/TrailBlaze'
import { useCart } from './context/cartcontext'
import { useLocation } from 'react-router-dom'

export default function ProductsPage() {
  const { PRODUCTS } = useCart()
  const location = useLocation()

  return (
    <div className="min-h-screen bg-parchment-100 flex flex-col">
      <Header />
      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-8">
        <h1 className="font-display italic text-2xl font-semibold text-ridge-800 mb-5">All Gear</h1>
        <div className="inventory_list grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {PRODUCTS.map((p) => (
            <ProductCard key={p.slug} product={p} />
          ))}
        </div>
      </main>
    </div>
  )
}