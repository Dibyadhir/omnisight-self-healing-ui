import { Routes, Route, Navigate } from 'react-router-dom'
import { CartProvider } from './context/cartcontext'
import LoginPage from './pages/loginpage'
import HomePage from './pages/homepage'
import ProductsPage from './pages/productpage'
import ProductDetailPage from './pages/productDetailpage'
import CartPage from './pages/CartPage'
import CheckoutPage from './pages/CheckoutPage'
import CheckoutCompletePage from './pages/CheckoutCompletePage'

export default function App() {
  return (
    <CartProvider>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/products/:slug" element={<ProductDetailPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/checkout-complete" element={<CheckoutCompletePage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </CartProvider>
  )
}
