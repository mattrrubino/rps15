//import "./Login.css" |  
import { useNavigate } from "react-router-dom"

const Login = () => {
    const navigate = useNavigate();
    return (
    <>
     <link rel="stylesheet" href="../src/Pages/Login.css" />
        <div className="login-container">

            <div className="login-flex-container" />
                <div className="flex-item">
                <p className="logo">Account Login</p>
                </div>

                <form className="login-form">
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
                <div className="flex-item button-flex-container">
                    <button type="button" id="create-account" className="form-button" onClick={() => navigate('../CreateAccount')}>
                    Create Account
                    </button>
                    <button type="submit" id="submit" className="form-button">
                    Submit
                    </button>
                    <button type="submit" id="forgot-password" className="form-button">
                    Forgot Password
                    </button>
                </div>
                </form>
        </div>
    </>
    )
}

export default Login