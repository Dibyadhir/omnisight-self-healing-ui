import { createContext, useContext, useState } from 'react'

const CartContext = createContext(null)

const PRODUCTS = [
  {
    slug: 'trailpack-40l',
    name: 'TrailPack 40L',
    price: 129.0,
    category: 'Packs',
    description:
      'A weatherproof 40-liter backpack built for multi-day hikes, with a padded hip belt and external lash points for extra gear.',
  },
  {
    slug: 'summit-tent-2p',
    name: 'Summit Tent 2P',
    price: 219.0,
    category: 'Shelter',
    description:
      'A 2-person, 3-season tent that pitches in under five minutes and packs down to the size of a loaf of bread.',
  },
  {
    slug: 'ember-camp-stove',
    name: 'Ember Camp Stove',
    price: 54.5,
    category: 'Cooking',
    description:
      'A compact folding stove that boils half a liter of water in ninety seconds, rain or shine.',
  },
  {
    slug: 'trekking-poles',
    name: 'Driftwood Trekking Poles',
    price: 78.0,
    category: 'Accessories',
    description:
      'Carbon-fiber poles with cork grips, adjustable from 24" to 55" for any trail or trekker.',
  },
]

export function CartProvider({ children }) {
  const [items, setItems] = useState([])
  const [customer, setCustomer] = useState({ firstName: '', lastName: '', postalCode: '' })

  function addToCart(product) {
    setItems((prev) => {
      const existing = prev.find((i) => i.slug === product.slug)
      if (existing) {
        return prev.map((i) => (i.slug === product.slug ? { ...i, qty: i.qty + 1 } : i))
      }
      return [...prev, { ...product, qty: 1 }]
    })
  }

  function removeFromCart(slug) {
    setItems((prev) => prev.filter((i) => i.slug !== slug))
  }

  function clearCart() {
    setItems([])
  }

  const itemTotal = items.reduce((sum, i) => sum + i.price * i.qty, 0)
  const tax = itemTotal * 0.08
  const total = itemTotal + tax

  return (
    <CartContext.Provider
      value={{ items, addToCart, removeFromCart, clearCart, itemTotal, tax, total, customer, setCustomer, PRODUCTS }}
    >
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used within CartProvider')
  return ctx
}
