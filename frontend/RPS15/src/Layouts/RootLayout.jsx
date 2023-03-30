import { NavLink, Outlet } from "react-router-dom"

export default function RootLayout() {
  return (
    <div className="root-layout">
        {/* <header>
            <nav>
                <h1>RPS-15</h1>
                <NavLink to="/">Home</NavLink>
                <NavLink to="Profile">Profile</NavLink>
            </nav>
        </header> */}

        <main>
            <Outlet />
        </main>
    </div>
  )
}
