import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { TrailMark } from '../components/TrailBlaze'

const VALID_USER = { username: 'standard_user', password: 'secret_sauce' }

export default function LoginPage() {
  const [error, setError] = useState('')
  const navigate = useNavigate()

  function handleLogin(e) {
    e.preventDefault()
    const form = new FormData(e.target)
    const username = form.get('username')
    const password = form.get('password')
    if (username === VALID_USER.username && password === VALID_USER.password) {
      setError('')
      navigate('/home')
    } else {
      setError('Incorrect username or password.')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-10 bg-parchment-100">
      <div className="w-full max-w-sm">
        <div className="flex items-center justify-center gap-2 mb-6">
          <TrailMark />
          <span className="font-display italic text-2xl font-semibold text-ridge-800 tracking-tight">
            TrekKart
          </span>
        </div>

        <form
          onSubmit={handleLogin}
          className="bg-parchment-50 border-2 border-ridge-800/10 rounded-xl p-7"
        >
          <p className="font-stamp text-[10px] uppercase tracking-[0.15em] text-ridge-800/50 text-center mb-6">
            Trailhead Sign-In
          </p>

          <div className="mb-4">
            <label htmlFor="user-name" className="block text-sm font-medium text-ridge-800 mb-1.5">
              Username
            </label>
            <input
              id="user-name"
              name="username"
              autoComplete="username"
              className="w-full bg-white border border-ridge-800/15 rounded-md px-3 py-2.5 text-sm text-ridge-800 focus:border-blaze-amber transition-colors"
            />
          </div>
          <div className="mb-5">
            <label htmlFor="password" className="block text-sm font-medium text-ridge-800 mb-1.5">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              className="w-full bg-white border border-ridge-800/15 rounded-md px-3 py-2.5 text-sm text-ridge-800 focus:border-blaze-amber transition-colors"
            />
          </div>

          {error && (
            <p className="error-message-container text-sm text-blaze-rust mb-4" role="alert">
              {error}
            </p>
          )}

          <button
            id="login-button"
            type="submit"
            className="w-full bg-ridge-800 hover:bg-ridge-900 text-parchment-50 font-medium rounded-md py-2.5 text-sm transition-colors"
          >
            Log in
          </button>

          <p className="font-stamp text-[10px] text-center text-ridge-800/40 mt-5 tracking-wide">
            standard_user / secret_sauce
          </p>
        </form>
      </div>
    </div>
  )
}