import {
  Route,
  Routes,
  BrowserRouter
} from 'react-router-dom'
import Home from './Pages/Home'
import viteLogo from '/vite.svg'
import { useState } from 'react'
import Login from './Pages/Login'
import Profile from './Pages/Profile'
import reactLogo from './assets/react.svg'
import RootLayout from './Layouts/RootLayout'
import CreateAccount from './Pages/CreateAccount'
// Clean imports babyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<RootLayout />}>
          <Route index element={<Home />} />
          <Route path='login' element={Login} />
          <Route path='createaccount' element={<CreateAccount />} />
          <Route path='profile' element={<Profile />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
