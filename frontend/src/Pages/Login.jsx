import './Login.css'
import { Link, useNavigate } from "react-router-dom"

const Login = () => {
    const navigate = useNavigate()

    function onCreateAccount() {
        navigate('../CreateAccount')
    }

    function onLogout() {
        var xhr = new XMLHttpRequest()
        xhr.open("POST", "/api/logout")

        xhr.onreadystatechange = () => {
            if (xhr.readyState != XMLHttpRequest.DONE) {
                return
            }

            const status = xhr.status;
            if (status === 200) {
                navigate("/")
            } else {
                alert("Not logged in")
            }
        }

        xhr.send()
    }

    function onSubmit() {
        var xhr = new XMLHttpRequest()
        xhr.open("POST", "/api/login")

        xhr.onreadystatechange = () => {
            if (xhr.readyState != XMLHttpRequest.DONE) {
                return
            }

            const status = xhr.status;
            if (status === 200) {
                navigate("/")
            } else {
                alert("Incorrect username or password.")
            }
        }

        var formData = new FormData(document.getElementById("login-form"))
        xhr.send(formData)
    }

    return (
        <div>
            <Link to="/">
                <div className="login--page--backBtn">🪨</div>
            </Link>
            <div className="login-container">

                <div className="login-flex-container">

                    <div className="flex-item">
                        <p className="logo">Account Login</p>
                    </div>

                    <form className="flex-item login-form" id="login-form">
                        <div className="flex-item">
                            <label htmlFor="username">Username:</label>
                            <input
                            type="text"
                            id="username"
                            name="username"
                            className="form-input"
                            required=""
                            />
                        </div>
                        <br/>
                        <div className="flex-item">
                            <label htmlFor="password">Password:</label>
                            <input
                            type="password"
                            id="password"
                            name="password"
                            className="form-input"
                            required=""
                            />
                        </div>
                        <br/>
                        <div className="flex-item button-flex-container">
                            <button type="button" id="create-account" className="form-button" onClick={onCreateAccount}>
                            Create Account
                            </button>

                            <button type="button" id="submit" className="form-button" onClick={onSubmit}>
                            Submit
                            </button>

                            <button type="button" id="log-out" className="form-button" onClick={onLogout}>
                            Log Out
                            </button>
                        </div>
                    </form>

                </div>
            </div>
        </div>
    )
}

export default Login