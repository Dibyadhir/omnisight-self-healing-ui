import { Link } from 'react-router-dom'
import Header from '../components/Header'
import { Blaze, TRAIL_STEPS } from '../components/TrailBlaze'

export default function CheckoutCompletePage() {
  return (
    <div className="min-h-screen bg-parchment-100 flex flex-col">
      <Header />
      <main className="flex-1 max-w-md w-full mx-auto px-6 py-16 flex flex-col items-center text-center">
        <div className="flex gap-1 mb-6">
          {TRAIL_STEPS.map((s) => <Blaze key={s.key} state="done" />)}
        </div>
        <h1 className="complete-header font-display italic text-2xl font-semibold text-ridge-800 mb-2">
          Thank you for your order!
        </h1>
        <p className="complete-text text-ridge-800/60 text-sm mb-6">
          Your gear is being packed for the trail.
        </p>
        <Link
          to="/products"
          className="font-stamp text-xs uppercase tracking-wide text-blaze-amber hover:text-blaze-rust"
        >
          Back to shop
        </Link>
      </main>
    </div>
  )
}